import streamlit as st
from PIL import Image
from datetime import datetime
import pandas as pd
import re  # For regex operations


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
    
def parse_questions_and_answers(file_contents):
    """
    Parses the script from the uploaded .txt file to map questions to their answers.
    The script is expected to be structured with each question followed by its answers,
    where each answer is prefixed with a dash.
    """
    qa_dict = {}  # Initialize an empty dictionary to store question-answer mappings
    question_number = 0  # Initialize question number tracking

    lines = file_contents.split('\n')
    for line in lines:
        if re.match(r"^\d+\.", line):  # Matches lines that start with a number followed by a dot
            question_number += 1
            question_text = line.split('.', 1)[1].strip()  # Extract question text
            qa_dict[f'FlowNo_{question_number}'] = {'question': question_text, 'answers': []}
        elif line.startswith("   - "):  # Identifies answer options
            answer = line.strip("   - ")
            if question_number > 0:
                qa_dict[f'FlowNo_{question_number}']['answers'].append(answer)

    return qa_dict

def custom_sort(col):
    match = re.match(r"FlowNo_(\d+)=*(\d*)", col)
    if match:
        question_num = int(match.group(1))
        flow_no = int(match.group(2)) if match.group(2) else 0
        return (question_num, flow_no)
    else:
        return (float('inf'), 0)

def run():
    st.title('Keypresses Decoder')
    
    # Initialize qa_dict in session_state if not present
    if 'qa_dict' not in st.session_state:
        st.session_state['qa_dict'] = {}
        
    if 'renamed_data' in st.session_state:
        renamed_data = st.session_state['renamed_data']
        
        # File uploader to allow users to upload a .txt file with scripts
        uploaded_file = st.file_uploader("Choose a file", type='txt')
        if uploaded_file is not None:
            # Reading the uploaded file and storing its contents
            file_contents = uploaded_file.getvalue().decode("utf-8")
            st.session_state['qa_dict'] = parse_questions_and_answers(file_contents)
            st.success("Questions and answers parsed successfully.")
        else:
            # Optional: Inform the user to upload a file
            st.info("Please upload a file to parse questions and their answers.")
        
        st.markdown("## Preview of questions and their answers.")
        if 'qa_dict' in st.session_state:
            qa_dict = st.session_state['qa_dict']
            sorted_columns = sorted(renamed_data.columns, key=custom_sort)
            renamed_data = renamed_data[sorted_columns]

            st.write("Preview of Renamed Data:")
            st.dataframe(renamed_data.head())

            keypress_mappings = {}
            drop_cols = []
            
            for col in renamed_data.columns[1:-1]:  # Iterate through DataFrame columns
                st.subheader(f"Question: {col}")
                if col in qa_dict.keys():
                    # This block is adjusted to use qa_dict for automated mapping
                    unique_values = qa_dict[col]  # Get unique answers from qa_dict
                    sorted_unique_values = sorted(unique_values, key=lambda x: (int(x.split('=')[1]) if x != '' else float('inf')))
                    container = st.container()
                    if container.checkbox(f"Exclude entire Question: {col}", key=f"exclude_{col}"):
                        drop_cols.append(col)
                        continue
            
                    container = st.container()
                    all_mappings = {}
                    drop_vals = []  # To hold flowno values to drop
                    
                    # Use parsed answers for initial mapping, allowing manual adjustments
                    if col in qa_dict:
                        for idx, val in enumerate(qa_dict[col]):
                            flow_no = f"{col}={idx+1}"
                            # Option to exclude specific flow no.
                            if container.checkbox(f"Exclude flowno '{flow_no}'", key=f"exclude_{flow_no}"):
                                drop_vals.append(flow_no)
                                continue
                            # Pre-fill with parsed answer, allowing manual edit
                            readable_val = container.text_input(f"Rename '{flow_no}' to:", value=val, key=f"rename_{flow_no}")
                            if readable_val:
                                all_mappings[flow_no] = readable_val
                    
                    # Apply mappings only if they are not flagged to be dropped
                    for val in drop_vals:
                        if val in all_mappings:
                            del all_mappings[val]

                    if all_mappings:
                        keypress_mappings[col] = all_mappings
            
            if st.button("Decode Keypresses"):
                for col, col_mappings in keypress_mappings.items():
                    if col not in drop_cols:  # Only apply mappings if the column is not excluded
                        renamed_data[col] = renamed_data[col].map(col_mappings).fillna(renamed_data[col])

                # Drop excluded columns
                renamed_data.drop(columns=drop_cols, inplace=True)
                
                drop_vals = {}
                
                # Now drop rows based on excluded FlowNo values
                for col, vals_to_drop in drop_vals.items():
                    for val in vals_to_drop:
                        renamed_data = renamed_data[renamed_data[col] != val]

                st.session_state['decoded_data'] = renamed_data
                
                # Display IVR length and shape
                st.write(f'IVR Length: {len(renamed_data)} rows')
                st.write(renamed_data.shape)

                # Current date for reporting
                today = datetime.now()
                st.write(f'IVR count by Set as of {today.strftime("%d-%m-%Y").replace("-0", "-")}')
                st.write(renamed_data['Set'].value_counts())  # Replace 'Set' with the actual column name for 'Set' data

                # Check for null values before dropping
                st.write(f'Before dropping: {len(renamed_data)} rows')
                renamed_data.dropna(inplace=True)
                st.write(f'After dropping: {len(renamed_data)} rows')
                st.write(f'Preview of Total of Null Values per Column:')
                st.write(renamed_data.isnull().sum())

                # Sanity check
                for col in renamed_data.columns:
                    st.write(f"Sanity check for {col}:")
                    st.write(renamed_data[col].value_counts(normalize=True))
                    st.write("\n")
                    
                st.write("Preview of Decoded Data:")
                st.dataframe(renamed_data)

                # CSV Download
                formatted_date = datetime.now().strftime("%Y%m%d")
                default_filename = f'IVR_Petaling_Jaya_Survey2023_Decoded_Data_v{formatted_date}.csv'
                output_filename = st.text_input("Edit the filename for download", value=default_filename)
                if not output_filename.lower().endswith('.csv'):
                    output_filename += '.csv'

                data_as_csv = renamed_data.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Decoded Data as CSV",
                    data=data_as_csv,
                    file_name=output_filename,
                    mime='text/csv'
                )

        else:
            st.error("No renamed data found. Please go back to the previous step and rename your data first.")

if __name__ == "__main__":
    run()
