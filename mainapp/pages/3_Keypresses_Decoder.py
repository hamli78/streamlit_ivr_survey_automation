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

import streamlit as st
import pandas as pd
import re

def custom_sort(col):
    match = re.match(r"FlowNo_(\d+)=*(\d*)", col)
    if match:
        question_num = int(match.group(1))  # Question number
        flow_no = int(match.group(2)) if match.group(2) else 0  # Flow number, default to 0 if not present
        return (question_num, flow_no)
    else:
        return (float('inf'), 0)


def run():
    st.title('Keypresses Decoder')

    if 'renamed_data' in st.session_state:
        renamed_data = st.session_state['renamed_data']
        
        # Automatically rename FlowNo based on 'qa_dict' if it exists in the session state
        if 'qa_dict' in st.session_state:
            qa_dict = st.session_state['qa_dict']
            # Create a mapping function to rename columns based on qa_dict
            def rename_flow_no(col):
                match = re.match(r"FlowNo_(\d+)=*(\d*)", col)
                if match:
                    question_num, flow_no = match.groups()
                    # Retrieve the renaming pattern from qa_dict
                    # Assume qa_dict now has a more direct mapping for renaming
                    # e.g., {'1': {'question': 'Q1 Text', 'answers': {'1': 'NewNameForFlow1', '2': 'NewNameForFlow2'}}}
                    new_name = qa_dict.get(str(question_num), {}).get('answers', {}).get(str(flow_no), "")
                    if new_name:
                        # If a new name is specified in the qa_dict, use it to rename the column
                        return f"FlowNo_{question_num}={new_name}"
                    else:
                        # If no new name is specified, return the column name as is
                        return col
                else:
                    return col

            # Apply the renaming
            renamed_data.columns = [rename_flow_no(col) for col in renamed_data.columns]
        
        # Sort columns based on custom criteria after potential renaming
        sorted_columns = sorted(renamed_data.columns, key=custom_sort)
        renamed_data = renamed_data[sorted_columns]
        
        st.write("Preview of Renamed Data:")
        st.dataframe(renamed_data.head())

        keypress_mappings = {}
        drop_cols = []

        for col in renamed_data.columns[1:-1]:
            st.subheader(f"Question: {col}")
            unique_values = renamed_data[col].unique()
            sorted_unique_values = sorted(unique_values, key=lambda x: (int(x.split('=')[1]) if x != '' else float('inf')))
            container = st.container()
            
            if container.checkbox(f"Exclude entire Question: {col}", key=f"exclude_{col}"):
                drop_cols.append(col)
                continue

            all_mappings = {}
            drop_vals = []  # To hold flowno values to drop
            
            for val in sorted_unique_values:
                if pd.notna(val):
                    # Automatically determine the rename value based on qa_dict
                    # Extract question and flow numbers from the column name
                    question_no, flow_no_val = re.match(r"FlowNo_(\d+)=*(\d*)", col)
                    default_rename_val = qa_dict.get(question_no, {}).get(flow_no_val, "")
                    
                    # Use the default value if available, or leave blank if not
                    readable_val = st.text_input(f"Rename '{val}' to:", value=default_rename_val, key=f"{col}_{val}")
                    if readable_val and readable_val != val:
                        all_mappings[val] = readable_val
                    elif not readable_val:  # If the box is intentionally left blank, assume exclusion
                        drop_vals.append(val)
            
            # Apply the mappings and exclusions
            keypress_mappings[col] = {val: name for val, name in all_mappings.items() if val not in drop_vals}

        if st.button("Decode Keypresses"):
            for col, col_mappings in keypress_mappings.items():
                if col not in drop_cols:
                    renamed_data[col] = renamed_data[col].map(col_mappings).fillna(renamed_data[col])

            renamed_data.drop(columns=drop_cols, inplace=True)

            st.session_state['decoded_data'] = renamed_data

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
