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
    
def run():

    if 'renamed_data' in st.session_state:
        renamed_data = st.session_state['renamed_data']
        
        # Sort columns based on custom criteria
        sorted_columns = sorted(renamed_data.columns, key=custom_sort)
        renamed_data = renamed_data[sorted_columns]
        
        st.write("Preview of Renamed Data:")
        st.dataframe(renamed_data.head())

        keypress_mappings = {}
        drop_cols = []
        excluded_flow_nos = {}  # Initialize here for the whole session

        # Extract the relevant columns (excluding the first and last non-question columns).
        question_columns = renamed_data.columns[1:-1]
        
        with st.expander("Show Unique Values for FlowNo"):
                for col in question_columns:
                    if col in renamed_data.columns:  # Ensure the column exists
                        st.write(f"Unique Values in {col} before mapping:", renamed_data[col].unique())
                        
        st.write("P/S : After uploading the file, You can review the Unique FlowNo above and check if got any unique FlowNo that is not in the original Script;(it might be due to the user mispressed the key), or drop questions that you don't want to include(analyze) in the DataFrame. Additionally, you can remove any FlowNo entries that don't exist in the script due to mistaken extra keypress entries made by the call center during the campaign that is not alligned with the original script.")
           
        for i, col in enumerate(question_columns, start=1):
            st.subheader(f"Q{i}: {col}")
            unique_values = renamed_data[col].unique()
            
            # Handle cases where values do not follow the 'key=value' format
            def sort_key(x):
                parts = x.split('=')
                if len(parts) > 1 and parts[1] != '':
                    return int(parts[1])
                else:
                    return float('inf')
                
            sorted_unique_values = sorted(unique_values, key=sort_key)
            
            # Checkbox to exclude entire question using question number instead of column name
            if st.checkbox(f"Drop entire Question {i}", key=f"exclude_{col}"):
                drop_cols.append(col)
                continue
                
            all_mappings = {}
            excluded_flow_nos[col] = []

            for idx, val in enumerate(sorted_unique_values):
                if pd.notna(val):
                    autofill_value = simple_mappings.get(val, "")
                    unique_key = f"{col}_{val}_{idx}"
                    
                    # Checkbox to decide whether to exclude this specific FlowNo value
                    if st.checkbox(f"Drop '{val}'", key=f"exclude_{unique_key}"):
                        excluded_flow_nos[col].append(val)
                        continue
                    
                    readable_val = st.text_input(f"Rename '{val}' to:", value=autofill_value, key=unique_key)
                    if readable_val:
                        all_mappings[val] = readable_val

            if all_mappings:
                keypress_mappings[col] = all_mappings

        if st.button("Decode Keypresses"):
            
            # Use an expander for optional debugging output
            with st.expander("Show keypress mappings"):
                st.write("Applying Debugging Details:", keypress_mappings)
                
            # Drop entire questions if needed
            if drop_cols:
                renamed_data.drop(columns=drop_cols, inplace=True)
                
            # Apply mappings and exclude specific FlowNo values
            for col, col_mappings in keypress_mappings.items():
                if col in renamed_data.columns:  # Ensure column exists
                    
                    # Debugging: Verify mappings are correct just before applying###############
                    # st.write(f"Applying mappings for {col}: {col_mappings}")
                    
                    renamed_data[col] = renamed_data[col].map(col_mappings).fillna(renamed_data[col])
                    if col in excluded_flow_nos:
                        for val_to_exclude in excluded_flow_nos[col]:
                            renamed_data = renamed_data[renamed_data[col] != val_to_exclude]
                            
            # Insert the classify_income function right before the CSV download logic
            if 'IncomeRange' in renamed_data.columns:
                # Classify income and store in a temporary column
                income_group = renamed_data['IncomeRange'].apply(classify_income)
                
                # Find the index of 'IncomeRange' column
                income_range_index = renamed_data.columns.get_loc('IncomeRange')
                
                # Insert 'IncomeGroup' column right after 'IncomeRange' column
                renamed_data.insert(income_range_index + 1, 'IncomeGroup', income_group)
            else:
                st.warning("IncomeRange column not found. Please ensure your data includes this column for income classification.")

            st.session_state['decoded_data'] = renamed_data  # Save updated DataFrame to session state
            
            # Display updated DataFrame and other information

            st.write("Preview of Decoded Data:")
            st.dataframe(renamed_data)
            
            # Display IVR length and shape
            st.write(f'IVR Length: {len(renamed_data)} rows')
            st.write(renamed_data.shape)

            # Current date for reporting
            today = datetime.now()
            st.write(f'IVR count by Set as of {today.strftime("%d-%m-%Y").replace("-0", "-")}')
            st.write(renamed_data['Set'].value_counts())  # Replace 'Set' with the actual column name for 'Set' data
            
            # Check for null values 
            st.markdown("### Null Values Inspection")
            renamed_data.dropna(inplace=True)
            st.write(f'No. of rows after dropping nulls: {len(renamed_data)} rows')
            st.write(f'Preview of Total of Null Values per Column:')
            st.write(renamed_data.isnull().sum())
            
            st.markdown("### Sanity check for values in each column")
            for col in renamed_data.columns:
                if col != 'phonenum':
                    st.write(renamed_data[col].value_counts(normalize=True))
                    st.write("\n")
            
            st.write("Preview of Decoded Data:")
            st.dataframe(renamed_data)

            # Initialize session state for output_filename if it doesn't already exist
            if 'output_filename' not in st.session_state:
                formatted_date = datetime.now().strftime("%Y%m%d")
                st.session_state['output_filename'] = f'IVR_Decoded_Data_v{formatted_date}.csv'

            # Function to update the filename in session state based on user input
            def update_output_filename():
                if st.session_state.output_filename_input and not st.session_state.output_filename_input.lower().endswith('.csv'):
                    st.session_state.output_filename = st.session_state.output_filename_input + '.csv'
                else:
                    st.session_state.output_filename = st.session_state.output_filename_input

            # User input for editing the filename, tied directly to session state
            st.text_input("Edit the filename for download", value=st.session_state['output_filename'], key='output_filename_input', on_change=update_output_filename)

            # Assuming renamed_data is defined elsewhere and is the data you want to download
            data_as_csv = renamed_data.to_csv(index=False).encode('utf-8')

            # Use the session state for the filename in the download button
            st.download_button(
                label="Download Decoded Data as CSV",
                data=data_as_csv,
                file_name=st.session_state['output_filename'],
                mime='text/csv'
            )

    else:
        st.error("No renamed data found. Please go back to the previous step and rename your data first.")

if __name__ == "__main__":
    run()
