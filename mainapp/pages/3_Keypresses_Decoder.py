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

def custom_sort(col):
    # Improved regex to capture question and flow numbers accurately
    match = re.match(r"FlowNo_(\d+)=*(\d*)", col)
    if match:
        question_num = int(match.group(1))  # Question number
        flow_no = int(match.group(2)) if match.group(2) else 0  # Flow number, default to 0 if not present
        return (question_num, flow_no) 
    else:
        # Return a tuple that sorts non-matching columns to the end
        return (float('inf'), 0)


def run():
    st.title('Keypresses Decoder')

    if 'renamed_data' in st.session_state:
        renamed_data = st.session_state['renamed_data']
        
        # Sort columns based on custom criteria
        sorted_columns = sorted(renamed_data.columns, key=custom_sort)
        renamed_data = renamed_data[sorted_columns]
        
        st.write("Preview of Renamed Data:")
        st.dataframe(renamed_data.head())

        keypress_mappings = {}
        drop_cols = []

        for col in renamed_data.columns[1:-1]:
            st.subheader(f"Question: {col}")
            unique_values = renamed_data[col].unique()
             
            # Sort the unique values in ascending order assuming they are integers
            sorted_unique_values = sorted(unique_values, key=lambda x: (int(x.split('=')[1]) if x != '' else float('inf')))
            container = st.container()
            # Checkbox to exclude entire question
            if container.checkbox(f"Exclude entire Question: {col}", key=f"exclude_{col}"):
                drop_cols.append(col)
                continue
            
            container = st.container()
            all_mappings = {}
            drop_vals = []  # To hold flowno values to drop
            
            for val in sorted_unique_values:
                if pd.notna(val):
                    # Checkbox to exclude specific flowno
                    if container.checkbox(f"Exclude flowno '{val}'", key=f"exclude_{col}_{val}"):
                        drop_vals.append(val)
                        continue
                    
                    readable_val = container.text_input(f"Rename '{val}' to:", value="", key=f"{col}_{val}")
                    if readable_val:
                        all_mappings[val] = readable_val
                        
            # Remove the excluded flowno values from mappings
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


# ni yang later awal tak pakai dah pakai yg first sebb sama padan je no dia
# page3.py
# page3.py

# import streamlit as st
# import pandas as pd

# def run():
#     st.title('Keypresses Decoder')

#     if 'renamed_data' in st.session_state:
#         renamed_data = st.session_state['renamed_data']
#         st.write("Preview of Renamed Data:")
#         st.dataframe(renamed_data.head())

#         # Dictionary to hold the mappings
#         keypress_mappings = {}

#         # Iterate through each column in the DataFrame, skipping the first column (phonenum)
#         for col in renamed_data.columns[1:]:  # Start from the second column
#             st.subheader(f"Question: {col}")
#             # Get unique keypress values for the current column and sort them
#             unique_values = sorted(
#                 [val for val in renamed_data[col].unique() if pd.notna(val)],
#                 key=lambda x: int(x.split('=')[1])
#             )
#             # Create a container to hold the text inputs
#             container = st.container()
#             all_mappings = {}
#             # Iterate over unique values and create a text input for each
#             for val in unique_values:
#                 readable_val = container.text_input(f"Rename '{val}' to:", value="", key=f"{col}_{val}")
#                 if readable_val:  # Only add non-empty mappings
#                     all_mappings[val] = readable_val
#             if all_mappings:
#                 keypress_mappings[col] = all_mappings

#         # Button to apply the mappings and update the DataFrame
#         if st.button("Decode Keypresses"):
#             # Apply the mappings to the DataFrame
#             for col, col_mappings in keypress_mappings.items():
#                 renamed_data[col] = renamed_data[col].map(col_mappings).fillna(renamed_data[col])

#             # Save the updated DataFrame to the session state
#             st.session_state['decoded_data'] = renamed_data

#             # Display the updated DataFrame
#             st.write("Data with Decoded Keypresses:")
#             st.dataframe(renamed_data.head())

#             # Display the answer proportions for each question
#             for col in renamed_data.columns[1:]:  # Again, skip the first column (phonenum)
#                 st.write(f"Answer Proportions for {col}:")
#                 st.write(renamed_data[col].value_counts(normalize=True))
                
#     else:
#         st.error("No renamed data found. Please go back to the previous step and rename your data first.")

# if __name__ == "__main__":
#     run()

# page3.py

# import streamlit as st
# import pandas as pd

# def run():
#     st.title('Keypresses Decoder')

#     if 'renamed_data' in st.session_state:
#         renamed_data = st.session_state['renamed_data']
#         st.write("Preview of Renamed Data:")
#         st.dataframe(renamed_data.head())

#         # Dictionary to hold the mappings
#         keypress_mappings = {}

#         # List of columns to skip when creating input fields
#         columns_to_skip = ["phonenum", "Set"]

#         # Iterate through each column in the DataFrame, skipping specified columns
#         for col in renamed_data.columns:
#             if col in columns_to_skip:
#                 continue  # Skip the current column

#             st.subheader(f"Question: {col}")
#             # Get unique keypress values for the current column and sort them        ##################################### 320 n 360 n 322
#             unique_values = sorted(
#                 [val for val in renamed_data[col].unique() if pd.notna(val)],
#                 key=lambda x: int(x.split('=')[1])
#             )
#             # Create a container to hold the text inputs
#             container = st.container()
#             all_mappings = {}
#             # Iterate over unique values and create a text input for each
#             for val in unique_values:
#                 readable_val = container.text_input(f"Rename '{val}' to:", value="", key=f"{col}_{val}")
#                 if readable_val:  # Only add non-empty mappings
#                     all_mappings[val] = readable_val
#             if all_mappings:
#                 keypress_mappings[col] = all_mappings

#         # Button to apply the mappings and update the DataFrame
#         if st.button("Decode Keypresses"):
#             # Apply the mappings to the DataFrame
#             for col, col_mappings in keypress_mappings.items():
#                 renamed_data[col] = renamed_data[col].map(col_mappings).fillna(renamed_data[col])

#             # Save the updated DataFrame to the session state
#             st.session_state['decoded_data'] = renamed_data

#             # Display the updated DataFrame
#             st.write("Data with Decoded Keypresses:")
#             st.dataframe(renamed_data.head())

#             # Display the answer proportions for each question
#             for col in renamed_data.columns:
#                 if col in columns_to_skip:
#                     continue  # Skip the columns that do not have keypress mappings
#                 st.write(f"Answer Proportions for {col}:")
#                 proportions = renamed_data[col].value_counts(normalize=True)
#                 st.bar_chart(proportions)

#     else:
#         st.error("No renamed data found. Please go back to the previous step and rename your data first.")

# if __name__ == "__main__":
#     run()

# import streamlit as st
# import pandas as pd
# import re
# from datetime import datetime

# # Function to parse questions and their corresponding answers from the text file
# def parse_questions_and_answers(file_contents):
#     """
#     Parses the uploaded .txt file to extract questions and their corresponding answers.
#     Expected file format:
#         1. Question text
#         - Answer 1
#         - Answer 2
#         ...
#     Returns a dictionary where keys are 'Q1', 'Q2', ... and values are the question text and a list of answers.
#     """
#     qa_dict = {}
#     current_question = None
#     for line in file_contents.split('\n'):
#         line = line.strip()
#         if line.startswith('-'):  # This is an answer
#             if current_question:
#                 answer_text = line[1:].strip()
#                 qa_dict[current_question]['answers'].append(answer_text)
#         else:
#             match = re.match(r"(\d+)\.\s*(.*)", line)
#             if match:
#                 question_number, question_text = match.groups()
#                 current_question = f"Q{int(question_number)}"
#                 qa_dict[current_question] = {'question': question_text.strip(), 'answers': []}
#     return qa_dict

# # Function to customize sorting of columns, focusing on FlowNo
# def custom_sort(col):
#     match = re.match(r"FlowNo_(\d+)=*(\d*)", col)
#     if match:
#         question_num = int(match.group(1))
#         flow_no = int(match.group(2)) if match.group(2) else 0
#         return (question_num, flow_no)
#     else:
#         return (float('inf'), 0)

# def run():
#     st.title('Data Processing App')

#     uploaded_file = st.file_uploader("Choose a text file", type='txt')
#     if uploaded_file is not None:
#         file_contents = uploaded_file.getvalue().decode("utf-8")
#         qa_dict = parse_questions_and_answers(file_contents)
#         if st.button("Preview Parsed Questions and Answers"):
#             for q, info in qa_dict.items():
#                 st.write(f"{q}: {info['question']}")
#                 for ans in info['answers']:
#                     st.write(f"- {ans}")

#     # Placeholder for DataFrame loading and initial renaming logic
#     # Assuming DataFrame is already loaded into 'cleaned_data' for simplicity
    
#         # Logic for initial column renaming based on parsed questions would go here
#         # This part is skipped for brevity and assumed to be handled separately

#         # The provided script for processing FlowNo values and further manipulations
#         if 'renamed_data' in st.session_state:
#             renamed_data = st.session_state['renamed_data']
#             # Assuming 'renamed_data' is the DataFrame after initial column renaming

#             # Sort columns based on custom criteria
#             sorted_columns = sorted(renamed_data.columns, key=custom_sort)
#             renamed_data = renamed_data[sorted_columns]

#             st.write("Preview of Renamed Data:")
#             st.dataframe(renamed_data.head())

#             # Further processing of FlowNo and other operations as described
#             # This includes the decoding keypresses logic and CSV download functionality
#             # Place the rest of your provided script here

#     else:
#         st.error("No data found. Please upload and prepare your data first.")

# if __name__ == "__main__":
#     run()
