import streamlit as st
from PIL import Image
from datetime import datetime
import pandas as pd
import re  # For regex operations
import json

# Configure the default settings of the page.
icon = Image.open('./images/invoke_logo.png')
st.set_page_config(
    page_title='IVR Data Cleaner 🧮',
    layout="wide",
    page_icon=icon,
    initial_sidebar_state="expanded"
)

def set_dark_mode_css():
    dark_mode_css = """
    <style>
        html, body, [class*="View"] {
            color: #ffffff;  /* Text Color */
            background-color: #111111;  /* Background Color */
        }
        .stTextInput > div > div > input {
            color: #ffffff;
            background-color: #111111;
        }
        .stCheckbox > label {
            color: #ffffff;
        }
        /* Add other widget-specific styles here */
    </style>
    """
    st.markdown(dark_mode_css, unsafe_allow_html=True)

# Call the function to apply the dark mode CSS
set_dark_mode_css()

def parse_text_to_json(text_content):
    """
    Parses structured text containing survey questions and answers into a JSON-like dictionary.
    Adjusts FlowNo to start from 2 for the first question as specified.
    """
    import re

    # Initialize variables
    data = {}
    current_question = None

    # Regular expressions for identifying parts of the text
    question_re = re.compile(r'^(\d+)\.\s+(.*)')
    answer_re = re.compile(r'^\s+-\s+(.*)')

    for line in text_content.splitlines():
        question_match = question_re.match(line)
        answer_match = answer_re.match(line)

        if question_match:
            # New question found
            q_number, q_text = question_match.groups()
            current_question = f"Q{q_number}"
            data[current_question] = {"question": q_text, "answers": {}}
        elif answer_match and current_question:
            # Answer found for the current question
            answer_text = answer_match.groups()[0]
            # Assuming FlowNo starts at 2 for the first question and increments for each answer within a question
            flow_no = len(data[current_question]["answers"]) + 1
            # Adjusting FlowNo to start from 2 for the first question and increment accordingly for each answer
            flow_no_key = f"FlowNo_{int(q_number)+1}={flow_no}"
            data[current_question]["answers"][flow_no_key] = answer_text

    return data

def custom_sort(col):
    # Improved regex to capture question and flow numbers accurately
    match = re.match(r"FlowNo_(\d+)=*(\d*)", col)
    if match:
        question_num = int(match.group(1))  # Question number
        flow_no = int(match.group(2)) if match.group(2) else 0  # Flow number, default to 0 if not present
        return (question_num, flow_no) 
    else:
        return (float('inf'), 0)

st.title('Keypresses Decoder🔑')

st.markdown("### Upload Script OR JSON Files (.txt,.json format)")
# Add a file uploader at the beginning of your app
uploaded_file = st.file_uploader("Choose a txt with formatting or json with flow-mapping file", type=['txt','json'])

# Initialize a variable to hold the mappings
flow_no_mappings = {}

# Check if a file is uploaded
if uploaded_file is not None:
    file_content = uploaded_file.getvalue().decode("utf-8")
    try:
        if uploaded_file.type == "application/json":
            # Handle JSON file
            flow_no_mappings = json.loads(file_content)
        else:
            # Handle plain text file
            flow_no_mappings = parse_text_to_json(file_content)
        st.success("Questions and answers parsed successfully.✨")
    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
        # Optional: Inform the user to upload a file
        st.info("Please upload a file to parse questions and their answers.")

# Flatten the JSON structure to simplify the mapping access
simple_mappings = {k: v for question in flow_no_mappings.values() for k, v in question["answers"].items()}
for q_key, q_data in flow_no_mappings.items():
    for answer_key, answer_value in q_data["answers"].items():
        simple_mappings[answer_key] = answer_value

def classify_income(income):
    if income == 'RM4,850 & below':
        return 'B40'
    elif income == 'RM4,851 to RM10,960':
        return 'M40'
    elif income in ['RM15,040 & above', 'RM10,961 to RM15,039']:
        return 'T20'
# Main function to run the Streamlit app
def run():
    # Check for display content in session state and initialize if absent
    if 'display_content' not in st.session_state:
        st.session_state['display_content'] = []
    
    # Initialize 'output_filename' in session state with formatted date
    if 'output_filename' not in st.session_state:
        formatted_date = datetime.now().strftime("%Y%m%d")
        st.session_state['output_filename'] = f'IVR_Decoded_Data_{formatted_date}.csv'
        
    if 'renamed_data' in st.session_state:
        renamed_data = st.session_state['renamed_data']
        
        # Sort columns based on custom criteria
        sorted_columns = sorted(renamed_data.columns, key=custom_sort)
        renamed_data = renamed_data[sorted_columns]
        
        st.write("Preview of Renamed Data:")
        st.dataframe(renamed_data.head())
        
        # Process each question column for unique values and mappings
        process_question_columns(renamed_data)
        
        # Optional: Insert additional data processing steps here
        
        if st.button("Decode Keypresses"):
            apply_mappings_and_classifications(renamed_data)
            download_prepared_data(renamed_data)
    else:
        st.error("No renamed data found. Please go back to the previous step and rename your data first.")

# Function to process question columns for unique values and mappings
def process_question_columns(renamed_data):
    question_columns = renamed_data.columns[1:-1]
    for i, col in enumerate(question_columns, start=1):
        # Process each column for unique values and potential mappings
        process_unique_values(col, i, renamed_data)

# Function to apply mappings and classifications to the data
def apply_mappings_and_classifications(renamed_data):
    # Implement logic to apply keypress mappings and classifications
    # Example: Insert classify_income function logic here if applicable
    st.write("Decoding and classification logic would be implemented here.")

# Function to allow the user to download the prepared data
def download_prepared_data(renamed_data):
    # Use a form for filename editing and download
    with st.form("edit_and_download"):
        edited_filename = st.text_input("Edit the filename for download", value=st.session_state['output_filename'])
        submitted = st.form_submit_button("Apply Changes and Prepare Download")
        if submitted:
            finalize_download(edited_filename, renamed_data)

# Function to finalize and execute the download process
def finalize_download(edited_filename, renamed_data):
    if not edited_filename.lower().endswith('.csv'):
        edited_filename += '.csv'
    st.session_state['output_filename'] = edited_filename
    data_as_csv = renamed_data.to_csv(index=False).encode('utf-8')
    st.download_button("Download Decoded Data as CSV", data=data_as_csv, file_name=edited_filename, mime='text/csv')

# Function to process unique values in a column - Placeholder for detailed implementation
def process_unique_values(column, index, dataframe):
    # Placeholder for logic to process unique values in a column
    st.write(f"Processing unique values for column {column} would be implemented here.")

if __name__ == "__main__":
    run()