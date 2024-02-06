import streamlit as st
from PIL import Image
from modules.security_utils import check_password

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

## Call the function to apply the dark mode CSS
set_dark_mode_css()

# # Function to rename columns based on user input
# def rename_columns(df, new_column_names):
#     mapping = {old: new for old, new in zip(df.columns, new_column_names) if new}
#     return df.rename(columns=mapping, inplace=False)

# def run():
#     st.title('Questionnaire Definer')

#     if 'cleaned_data' in st.session_state:
#         cleaned_data = st.session_state['cleaned_data']
#         st.write("Preview of Cleaned Data:")
#         st.dataframe(cleaned_data.head())

#         # Create a two-column layout
#         col1, col2 = st.columns(2)

#         with col1:
#             st.write("Rename Columns:")
#             new_column_names = [st.text_input(f"Q{idx+1}:", value=col, key=f"new_name_{idx}") for idx, col in enumerate(cleaned_data.columns)]

#         with col2:
#             st.write(" ")  # Just to align with the left column

#         if st.button("Apply New Column Names"):
#             updated_df = rename_columns(cleaned_data, new_column_names)
#             st.session_state['renamed_data'] = updated_df  # Save the DataFrame with renamed columns

#             st.write("DataFrame with Renamed Columns:")
#             st.dataframe(updated_df.head())

#     else:
#         st.error("No cleaned data found. Please go back to the previous step and process your data first.")

# if __name__ == "__main__":
#     run()

#yang kedua

# import streamlit as st
# from PIL import Image
# import pandas as pd
# import re

# # Define the function to rename columns based on user input
# def rename_columns(df, new_column_names):
#     mapping = {old: new for old, new in zip(df.columns, new_column_names) if new}
#     return df.rename(columns=mapping, inplace=False)

# # Function to parse questions from the uploaded .txt file
# def parse_questions(file_contents):
#     """
#     Parses the uploaded .txt file to extract questions.
#     Expected file format:
#         1. Question 1 text
#         2. Question 2 text
#         ...
#     Returns a dictionary where keys are 'Q1', 'Q2', ... and values are the corresponding questions.
#     """
#     questions = {}
#     for line in file_contents.split('\n'):
#         match = re.match(r"(\d+)\.\s+(.*)", line)
#         if match:
#             question_number, question_text = match.groups()
#             questions[f"Q{question_number}"] = question_text.strip()
#     return questions

# def run():
#     st.title('Questionnaire Definer')

#     # File uploader to allow users to upload a .txt file with scripts
#     uploaded_file = st.file_uploader("Choose a file", type='txt')
#     if uploaded_file is not None:
#         # Reading the uploaded file and storing its contents
#         file_contents = uploaded_file.getvalue().decode("utf-8")
#         questions = parse_questions(file_contents)
#     else:
#         questions = {}

#     if 'cleaned_data' in st.session_state:
#         cleaned_data = st.session_state['cleaned_data']
#         st.write("Preview of Cleaned Data:")
#         st.dataframe(cleaned_data.head())

#         # Create a two-column layout
#         col1, col2 = st.columns(2)

#         with col1:
#             st.write("Rename Columns:")
#             new_column_names = []
#             for idx, col in enumerate(cleaned_data.columns):
#                 # Use the question from the uploaded file if available, otherwise use the existing column name
#                 default_value = questions.get(f"Q{idx+1}", col)
#                 new_name = st.text_input(f"Q{idx+1}:", value=default_value, key=f"new_name_{idx}")
#                 new_column_names.append(new_name)

#         with col2:
#             st.write(" ")  # Just to align with the left column

#         if st.button("Apply New Column Names"):
#             updated_df = rename_columns(cleaned_data, new_column_names)
#             st.session_state['renamed_data'] = updated_df  # Save the DataFrame with renamed columns

#             st.write("DataFrame with Renamed Columns:")
#             st.dataframe(updated_df.head())

#     else:
#         st.error("No cleaned data found. Please go back to the previous step and process your data first.")

# if __name__ == "__main__":
#     run()
    

# def run():
#     st.title('Questionnaire Definer')

#     # File uploader to allow users to upload a .txt file with scripts
#     uploaded_file = st.file_uploader("Choose a file", type='txt')
#     if uploaded_file is not None:
#         # Reading the uploaded file and storing its contents
#         file_contents = uploaded_file.getvalue().decode("utf-8")
#         questions = parse_questions(file_contents)
#     else:
#         questions = {}

#     if 'cleaned_data' in st.session_state:
#         cleaned_data = st.session_state['cleaned_data']
#         st.write("Preview of Cleaned Data:")
#         st.dataframe(cleaned_data.head())

#         # Create a two-column layout
#         col1, col2 = st.columns(2)

#         with col1:
#             st.write("Rename Columns:")
#             new_column_names = []
#             for idx, col in enumerate(cleaned_data.columns):
#                 if idx == 0:
#                     # Reserve Q0 for a specific column like "phonenum"
#                     default_value = "phonenum"
#                 else:
#                     # Adjusted to ensure questions start from Q1 for the first question
#                     default_value = questions.get(f"Q{idx}", col)
#                 new_name = st.text_input(f"Q{idx}:", value=default_value, key=f"new_name_{idx}")
#                 new_column_names.append(new_name)

#         with col2:
#             st.write(" ")  # Just to align with the left column

#         if st.button("Apply New Column Names"):
#             updated_df = rename_columns(cleaned_data, new_column_names)
#             st.session_state['renamed_data'] = updated_df  # Save the DataFrame with renamed columns

#             st.write("DataFrame with Renamed Columns:")
#             st.dataframe(updated_df.head())

#     else:
#         st.error("No cleaned data found. Please go back to the previous step and process your data first.")

# # ni yg terbaru 5 hari bulan yg betul
# import streamlit as st
# import re

# # Function to rename columns based on user input
# def rename_columns(df, new_column_names):
#     mapping = {old: new for old, new in zip(df.columns, new_column_names) if new}
#     return df.rename(columns=mapping, inplace=False)

# # Function to parse questions from the uploaded .txt file
# def parse_questions(file_contents):
#     """
#     Parses the uploaded .txt file to extract questions.
#     Expected file format:
#         1. Question text
#         2. Question text
#         ...
#     Returns a dictionary where keys are 'Q1', 'Q2', ... and values are the corresponding questions.
#     """
#     questions = {}
#     # Adjusting the logic to match your file format and expectations
#     for line in file_contents.split('\n'):
#         match = re.match(r"(\d+)\.\s*(.*)", line)
#         if match:
#             question_number, question_text = match.groups()
#             questions[f"Q{int(question_number)}"] = question_text.strip()  # Ensure numbering matches user expectation
#     return questions

# def run():
#     st.title('Questionnaire Definer')

#     # File uploader to allow users to upload a .txt file with scripts
#     uploaded_file = st.file_uploader("Choose a file", type='txt')
#     if uploaded_file is not None:
#         # Reading the uploaded file and storing its contents
#         file_contents = uploaded_file.getvalue().decode("utf-8")
#         questions = parse_questions(file_contents)
#     else:
#         questions = {}

#     if 'cleaned_data' in st.session_state:
#         cleaned_data = st.session_state['cleaned_data']
#         st.write("Preview of Cleaned Data:")
#         st.dataframe(cleaned_data.head())

#         # Create a two-column layout
#         col1, col2 = st.columns(2)

#         with col1:
#             st.write("Rename Columns:")
#             new_column_names = []
#             for idx, col in enumerate(cleaned_data.columns):
#                 if idx == 0:
#                     # Reserve Q0 for a specific column like "phonenum"
#                     default_value = "phonenum"
#                 else:
#                     # Adjusted to ensure questions start from Q1 for the first question, respecting the offset
#                     default_value = questions.get(f"Q{idx}", col)
#                 new_name = st.text_input(f"Column {idx}:", value=default_value, key=f"new_name_{idx}")
#                 new_column_names.append(new_name)

#         with col2:
#             st.write(" ")  # Just to align with the left column

#         if st.button("Apply New Column Names"):
#             updated_df = rename_columns(cleaned_data, new_column_names)
#             st.session_state['renamed_data'] = updated_df  # Save the DataFrame with renamed columns

#             st.write("DataFrame with Renamed Columns:")
#             st.dataframe(updated_df.head())

#     else:
#         st.error("No cleaned data found. Please go back to the previous step and process your data first.")

# if __name__ == "__main__":
#     run()


# # try2 yg sebelum ni betul punya , ni nak try combine in one page
# import streamlit as st
# import re
# from datetime import datetime
# import pandas as pd

# # Function to rename columns based on user input
# def rename_columns(df, new_column_names):
#     mapping = {old: new for old, new in zip(df.columns, new_column_names) if new}
#     return df.rename(columns=mapping, inplace=False)

# # Function to parse questions from the uploaded .txt file
# def parse_questions_and_answers(file_contents):
#     """
#     Parses the uploaded .txt file to extract questions and their corresponding answers.
#     Expected file format:
#         1. Question text
#         - Answer 1
#         - Answer 2
#         ...
#     Returns a dictionary where keys are 'Q{question_number}' and values are dictionaries
#     containing the question text and a list of its answers.
#     """
#     questions_and_answers = {}
#     current_question_key = None

#     for line in file_contents.split('\n'):
#         line = line.strip()
#         if line.startswith('-'):  # This line is an answer
#             answer_text = line[1:].strip()  # Remove the dash and leading whitespace
#             if current_question_key and answer_text:  # Make sure there's a question to attach this answer to
#                 questions_and_answers[current_question_key]['answers'].append(answer_text)
#         else:
#             match = re.match(r"(\d+)\.\s*(.*)", line)
#             if match:
#                 question_number, question_text = match.groups()
#                 current_question_key = f"Q{int(question_number)}"
#                 # Initialize the dictionary entry for this question with the question text and an empty list for answers
#                 questions_and_answers[current_question_key] = {'question': question_text.strip(), 'answers': []}

#     return questions_and_answers


# def run():
#     st.title('Questionnaire Definer')

#     # File uploader to allow users to upload a .txt file with scripts
#     uploaded_file = st.file_uploader("Choose a file", type='txt')
#     if uploaded_file is not None:
#         # Reading the uploaded file and storing its contents
#         file_contents = uploaded_file.getvalue().decode("utf-8")
#         qa_dict = parse_questions_and_answers(file_contents)  # Use the enhanced parsing function
#     else:
#         qa_dict = {}

#     # Example usage of the parsed questions and answers
#     if qa_dict:
#         for q_key, q_info in qa_dict.items():
#             st.subheader(f"{q_key}: {q_info['question']}")
#             for answer in q_info['answers']:
#                 st.write(f"- {answer}")
#     else:
#         st.write("Please upload a file to parse questions and their answers.")


#     if 'cleaned_data' in st.session_state:
#         cleaned_data = st.session_state['cleaned_data']
#         st.write("Preview of Cleaned Data:")
#         st.dataframe(cleaned_data.head())

#         # Create a two-column layout
#         col1, col2 = st.columns(2)

#         with col1:
#             st.write("Rename Columns:")
#             new_column_names = []
#             for idx, col in enumerate(cleaned_data.columns):
#                 if idx == 0:
#                     # Reserve Q0 for a specific column like "phonenum"
#                     default_value = "phonenum"
#                 else:
#                     # Adjusted to ensure questions start from Q1 for the first question, respecting the offset
#                     default_value = qa_dict.get(f"Q{idx}", {}).get('question', col)
#                 new_name = st.text_input(f"Column {idx}:", value=default_value, key=f"new_name_{idx}")
#                 new_column_names.append(new_name)

#         with col2:
#             st.write(" ")  # Just to align with the left column

#         if st.button("Apply New Column Names"):
#             updated_df = rename_columns(cleaned_data, new_column_names)
#             st.session_state['renamed_data'] = updated_df  # Save the DataFrame with renamed columns

#             st.write("DataFrame with Renamed Columns:")
#             st.dataframe(updated_df.head())

#     else:
#         st.error("No cleaned data found. Please go back to the previous step and process your data first.")

# def custom_sort(col):
#     # Improved regex to capture question and flow numbers accurately
#     match = re.match(r"FlowNo_(\d+)=*(\d*)", col)
#     if match:
#         question_num = int(match.group(1))  # Question number
#         flow_no = int(match.group(2)) if match.group(2) else 0  # Flow number, default to 0 if not present
#         return (question_num, flow_no) 
#     else:
#         # Return a tuple that sorts non-matching columns to the end
#         return (float('inf'), 0)

# def run():
#     st.title('Keypresses Decoder')

#     if 'renamed_data' in st.session_state:
#         renamed_data = st.session_state['renamed_data']
        
#         # Sort columns based on custom criteria
#         sorted_columns = sorted(renamed_data.columns, key=custom_sort)
#         renamed_data = renamed_data[sorted_columns]
        
#         st.write("Preview of Renamed Data:")
#         st.dataframe(renamed_data.head())

#         keypress_mappings = {}
#         drop_cols = []

#         for col in renamed_data.columns[1:-1]:
#             st.subheader(f"Question: {col}")
#             unique_values = renamed_data[col].unique()
             
#             # Sort the unique values in ascending order assuming they are integers
#             sorted_unique_values = sorted(unique_values, key=lambda x: (int(x.split('=')[1]) if x != '' else float('inf')))
#             container = st.container()
#             # Checkbox to exclude entire question
#             if container.checkbox(f"Exclude entire Question: {col}", key=f"exclude_{col}"):
#                 drop_cols.append(col)
#                 continue
            
#             container = st.container()
#             all_mappings = {}
#             drop_vals = []  # To hold flowno values to drop
            
#             for val in sorted_unique_values:
#                 if pd.notna(val):
#                     # Checkbox to exclude specific flowno
#                     if container.checkbox(f"Exclude flowno '{val}'", key=f"exclude_{col}_{val}"):
#                         drop_vals.append(val)
#                         continue
                    
#                     readable_val = container.text_input(f"Rename '{val}' to:", value="", key=f"{col}_{val}")
#                     if readable_val:
#                         all_mappings[val] = readable_val
                        
#             # Remove the excluded flowno values from mappings
#             for val in drop_vals:
#                 if val in all_mappings:
#                     del all_mappings[val]

#             if all_mappings:
#                 keypress_mappings[col] = all_mappings
            
#         if st.button("Decode Keypresses"):
#             for col, col_mappings in keypress_mappings.items():
#                 if col not in drop_cols:  # Only apply mappings if the column is not excluded
#                     renamed_data[col] = renamed_data[col].map(col_mappings).fillna(renamed_data[col])

#             # Drop excluded columns
#             renamed_data.drop(columns=drop_cols, inplace=True)
            
#             drop_vals = {}
            
#             # Now drop rows based on excluded FlowNo values
#             for col, vals_to_drop in drop_vals.items():
#                 for val in vals_to_drop:
#                     renamed_data = renamed_data[renamed_data[col] != val]

#             st.session_state['decoded_data'] = renamed_data
            
#             # Display IVR length and shape
#             st.write(f'IVR Length: {len(renamed_data)} rows')
#             st.write(renamed_data.shape)

#             # Current date for reporting
#             today = datetime.now()
#             st.write(f'IVR count by Set as of {today.strftime("%d-%m-%Y").replace("-0", "-")}')
#             st.write(renamed_data['Set'].value_counts())  # Replace 'Set' with the actual column name for 'Set' data

#             # Check for null values before dropping
#             st.write(f'Before dropping: {len(renamed_data)} rows')
#             renamed_data.dropna(inplace=True)
#             st.write(f'After dropping: {len(renamed_data)} rows')
#             st.write(f'Preview of Total of Null Values per Column:')
#             st.write(renamed_data.isnull().sum())

#             # Sanity check
#             for col in renamed_data.columns:
#                 st.write(f"Sanity check for {col}:")
#                 st.write(renamed_data[col].value_counts(normalize=True))
#                 st.write("\n")
                
#             st.write("Preview of Decoded Data:")
#             st.dataframe(renamed_data)

#             # CSV Download
#             formatted_date = datetime.now().strftime("%Y%m%d")
#             default_filename = f'IVR_Petaling_Jaya_Survey2023_Decoded_Data_v{formatted_date}.csv'
#             output_filename = st.text_input("Edit the filename for download", value=default_filename)
#             if not output_filename.lower().endswith('.csv'):
#                 output_filename += '.csv'

#             data_as_csv = renamed_data.to_csv(index=False).encode('utf-8')
#             st.download_button(
#                 label="Download Decoded Data as CSV",
#                 data=data_as_csv,
#                 file_name=output_filename,
#                 mime='text/csv'
#             )

#     else:
#         st.error("No renamed data found. Please go back to the previous step and rename your data first.")


# if __name__ == "__main__":
#     run()

# import streamlit as st
# import re
# from datetime import datetime
# import pandas as pd

# # Function to rename columns based on user input
# def rename_columns(df, new_column_names):
#     mapping = {old: new for old, new in zip(df.columns, new_column_names) if new}
#     return df.rename(columns=mapping, inplace=False)

# # Function to parse questions from the uploaded .txt file
# def parse_questions_and_answers(file_contents):
#     """
#     Parses the uploaded .txt file to extract questions and their corresponding answers.
#     Expected file format:
#         1. Question text
#         - Answer 1
#         - Answer 2
#         ...
#     Returns a dictionary where keys are 'Q{question_number}' and values are dictionaries
#     containing the question text and a list of its answers.
#     """
#     questions_and_answers = {}
#     current_question_key = None

#     for line in file_contents.split('\n'):
#         line = line.strip()
#         if line.startswith('-'):  # This line is an answer
#             answer_text = line[1:].strip()  # Remove the dash and leading whitespace
#             if current_question_key and answer_text:  # Make sure there's a question to attach this answer to
#                 questions_and_answers[current_question_key]['answers'].append(answer_text)
#         else:
#             match = re.match(r"(\d+)\.\s*(.*)", line)
#             if match:
#                 question_number, question_text = match.groups()
#                 current_question_key = f"Q{int(question_number)}"
#                 # Initialize the dictionary entry for this question with the question text and an empty list for answers
#                 questions_and_answers[current_question_key] = {'question': question_text.strip(), 'answers': []}

#     return questions_and_answers

# # Function to sort columns based on custom criteria
# def custom_sort(col):
#     # Improved regex to capture question and flow numbers accurately
#     match = re.match(r"FlowNo_(\d+)=*(\d*)", col)
#     if match:
#         question_num = int(match.group(1))  # Question number
#         flow_no = int(match.group(2)) if match.group(2) else 0  # Flow number, default to 0 if not present
#         return (question_num, flow_no)
#     else:
#         # Return a tuple that sorts non-matching columns to the end
#         return (float('inf'), 0)

# def run():
#     st.title('Keypresses Decoder')

#     if 'renamed_data' in st.session_state:
#         renamed_data = st.session_state['renamed_data']

#         # Sort columns based on custom criteria
#         sorted_columns = sorted(renamed_data.columns, key=custom_sort)
#         renamed_data = renamed_data[sorted_columns]

#         st.write("Preview of Renamed Data:")
#         st.dataframe(renamed_data.head())

#         keypress_mappings = {}
#         drop_cols = []

#         for col in renamed_data.columns[1:-1]:
#             st.subheader(f"Question: {col}")
#             unique_values = renamed_data[col].unique()

#             # Sort the unique values in ascending order assuming they are integers
#             sorted_unique_values = sorted(unique_values, key=lambda x: (int(x.split('=')[1]) if x != '' else float('inf')))
#             container = st.container()
#             # Checkbox to exclude entire question
#             if container.checkbox(f"Exclude entire Question: {col}", key=f"exclude_{col}"):
#                 drop_cols.append(col)
#                 continue

#             container = st.container()
#             all_mappings = {}
#             drop_vals = []  # To hold FlowNo values to drop

#             for val in sorted_unique_values:
#                 if pd.notna(val):
#                     # Checkbox to exclude specific FlowNo
#                     if container.checkbox(f"Exclude FlowNo '{val}'", key=f"exclude_{col}_{val}"):
#                         drop_vals.append(val)
#                         continue

#                     readable_val = container.text_input(f"Rename '{val}' to:", value="", key=f"{col}_{val}")
#                     if readable_val:
#                         all_mappings[val] = readable_val

#             # Remove the excluded FlowNo values from mappings
#             for val in drop_vals:
#                 if val in all_mappings:
#                     del all_mappings[val]

#             if all_mappings:
#                 keypress_mappings[col] = all_mappings

#         if st.button("Decode Keypresses"):
#             for col, col_mappings in keypress_mappings.items():
#                 if col not in drop_cols:  # Only apply mappings if the column is not excluded
#                     renamed_data[col] = renamed_data[col].map(col_mappings).fillna(renamed_data[col])

#             # Drop excluded columns
#             renamed_data.drop(columns=drop_cols, inplace=True)

#             drop_vals = {}

#             # Now drop rows based on excluded FlowNo values
#             for col, vals_to_drop in drop_vals.items():
#                 for val in vals_to_drop:
#                     renamed_data = renamed_data[renamed_data[col] != val]

#             st.session_state['decoded_data'] = renamed_data

#             # Display IVR length and shape
#             st.write(f'IVR Length: {len(renamed_data)} rows')
#             st.write(renamed_data.shape)

#             # Current date for reporting
#             today = datetime.now()
#             st.write(f'IVR count by Set as of {today.strftime("%d-%m-%Y").replace("-0", "-")}')
#             st.write(renamed_data['Set'].value_counts())  # Replace 'Set' with the actual column name for 'Set' data

#             # Check for null values before dropping
#             st.write(f'Before dropping: {len(renamed_data)} rows')
#             renamed_data.dropna(inplace=True)
#             st.write(f'After dropping: {len(renamed_data)} rows')
#             st.write(f'Preview of Total of Null Values per Column:')
#             st.write(renamed_data.isnull().sum())

#             # Sanity check
#             for col in renamed_data.columns:
#                 st.write(f"Sanity check for {col}:")
#                 st.write(renamed_data[col].value_counts(normalize=True))
#                 st.write("\n")

#             st.write("Preview of Decoded Data:")
#             st.dataframe(renamed_data)

#             # CSV Download
#             formatted_date = datetime.now().strftime("%Y%m%d")
#             default_filename = f'IVR_Petaling_Jaya_Survey2023_Decoded_Data_v{formatted_date}.csv'
#             output_filename = st.text_input("Edit the filename for download", value=default_filename)
#             if not output_filename.lower().endswith('.csv'):
#                 output_filename += '.csv'

#             data_as_csv = renamed_data.to_csv(index=False).encode('utf-8')
#             st.download_button(
#                 label="Download Decoded Data as CSV",
#                 data=data_as_csv,
#                 file_name=output_filename,
#                 mime='text/csv'
#             )

#     else:
#         st.error("No renamed data found. Please go back to the previous step and rename your data first.")

# if __name__ == "__main__":
#     run()

import streamlit as st
import re
from datetime import datetime
import pandas as pd

# Function to rename columns based on user input
def rename_columns(df, new_column_names):
    mapping = {old: new for old, new in zip(df.columns, new_column_names) if new}
    return df.rename(columns=mapping, inplace=False)

# Function to parse questions from the uploaded .txt file
def parse_questions_and_answers(file_contents):
    """
    Parses the uploaded .txt file to extract questions and their corresponding answers.
    Expected file format:
        1. Question text
        - Answer 1
        - Answer 2
        ...
    Returns a dictionary where keys are 'Q{question_number}' and values are dictionaries
    containing the question text and a list of its answers.
    """
    questions_and_answers = {}
    current_question_key = None

    for line in file_contents.split('\n'):
        line = line.strip()
        if line.startswith('-'):  # This line is an answer
            answer_text = line[1:].strip()  # Remove the dash and leading whitespace
            if current_question_key and answer_text:  # Make sure there's a question to attach this answer to
                questions_and_answers[current_question_key]['answers'].append(answer_text)
        else:
            match = re.match(r"(\d+)\.\s*(.*)", line)
            if match:
                question_number, question_text = match.groups()
                current_question_key = f"Q{int(question_number)}"
                # Initialize the dictionary entry for this question with the question text and an empty list for answers
                questions_and_answers[current_question_key] = {'question': question_text.strip(), 'answers': []}

    return questions_and_answers

# Function to sort columns based on custom criteria
def custom_sort(col):
    try:
        # Improved regex to capture question and flow numbers accurately
        match = re.match(r"FlowNo_(\d+)=*(\d*)", col)
        if match:
            question_num = int(match.group(1))  # Question number
            flow_no = int(match.group(2)) if match.group(2) else 0  # Flow number, default to 0 if not present
            return (question_num, flow_no)
    except Exception as e:
        pass  # Handle the case where the regex doesn't match
    # Return a tuple that sorts non-matching columns to the end
    return (float('inf'), 0)

def run1():
    st.title('Questionnaire Definer')
    
    # Check if 'qa_dict' is already in session state, otherwise initialize it
    if 'qa_dict' not in st.session_state:
        st.session_state['qa_dict'] = {}

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
    
     # Display parsed questions and answers if available
    if st.session_state['qa_dict']:
        for q_key, q_info in st.session_state['qa_dict'].items():
            st.subheader(f"{q_key}: {q_info['question']}")
            for answer in q_info['answers']:
                st.write(f"- {answer}")
    else:
        st.write("No questions and answers to display. Please upload a file.")

    if 'cleaned_data' in st.session_state:
        cleaned_data = st.session_state['cleaned_data']

        # Create a two-column layout
        col1, col2 = st.columns(2)

        with col1:
            st.write("Rename Columns:")
            new_column_names = []
            for idx, col in enumerate(cleaned_data.columns):
                if idx == 0:
                    # Reserve Q0 for a specific column like "phonenum"
                    default_value = "phonenum"
                else:
                    # Use qa_dict from st.session_state to get the default value for the text input
                    # Adjusted to ensure questions start from Q1 for the first question, respecting the offset
                    default_value = st.session_state['qa_dict'].get(f"Q{idx}", {}).get('question', col)
                new_name = st.text_input(f"Column {idx}:", value=default_value, key=f"new_name_{idx}")
                new_column_names.append(new_name)

        with col2:
            st.write(" ")  # Just to align with the left column

        if st.button("Apply New Column Names"):
            updated_df = rename_columns(cleaned_data, new_column_names)
            st.session_state['renamed_data'] = updated_df  # Save the DataFrame with renamed columns

            st.write("DataFrame with Renamed Columns:")
            st.dataframe(updated_df.head())

    else:
        st.error("No cleaned data found. Please go back to the previous step and process your data first.")
        
if __name__ == "__main__":
    run1()

def run2():
    st.title('Keypresses Decoder')

    if 'renamed_data' in st.session_state:
        renamed_data = st.session_state['renamed_data']  # Use the renamed_data from the previous step
        
        if 'qa_dict' not in st.session_state:
            st.error("Question and Answer data not loaded. Please go back and upload the text file.")
            return

        qa_dict = st.session_state['qa_dict']
        
        # Sort columns based on custom criteria
        sorted_columns = sorted(renamed_data.columns, key=custom_sort)
        renamed_data = renamed_data[sorted_columns]

        st.write("Preview of Renamed Data:")
        st.dataframe(renamed_data.head())

        keypress_mappings = {}
        drop_cols = []
        drop_vals = {}
        
        for col in renamed_data.columns[1:-1]:
            # Extract question number from the column name
            match = re.match(r"FlowNo_(\d+)", col)
            if match:
                question_number = int(match.group(1))
                q_key = f"Q{question_number}"
                
                if q_key in qa_dict:
                    question_info = qa_dict[q_key]
                    st.subheader(f"{q_key}: {question_info['question']}")
                    
                    container = st.container()
                    all_mappings = {}
                    
                    for i, answer in enumerate(question_info['answers'], start=1):
                        val = f"FlowNo_{question_number}={i}"
                        readable_val = container.text_input(f"Rename '{val}' to:", value=answer, key=f"{col}_{i}")
                        all_mappings[val.split('=')[0]] = readable_val
                    
                    # sorted_unique_values = [f"FlowNo_{question_number}={i+1}" for i in range(len(question_info['answers']))]
                    # container = st.container()

                    # all_mappings = {}
                    # for i, val in enumerate(sorted_unique_values):
                    #     readable_val = container.text_input(f"Rename '{val}' to:", value=question_info['answers'][i], key=f"{col}_{i+1}")
                    #     all_mappings[val] = readable_val

                    keypress_mappings[col] = all_mappings
                    
                if container.checkbox(f"Exclude entire Question: {col}", key=f"exclude_{col}"):
                    drop_cols.append(col)
                        
        if st.button("Decode Keypresses"):
            # Apply the mappings
            for col, mappings in keypress_mappings.items():
                for flow_val, new_name in mappings.items():
                    # Note: You may need to adjust the logic to apply the mapping directly to DataFrame values
                    renamed_data[col] = renamed_data[col].replace(to_replace=flow_val, value=new_name, regex=True)
                    # renamed_data[col] = renamed_data[col].replace(flow_val.split('=')[0], new_name)
            
            # Drop excluded columns
            renamed_data.drop(columns=drop_cols, inplace=True)

            st.session_state['decoded_data'] = renamed_data
            st.write("Preview of Decoded Data:")
            st.dataframe(renamed_data.head())
            st.session_state['decoded_data'] = renamed_data
           
            st.subheader(f"Question: {col}")
            unique_values = renamed_data[col].unique()

            # Sort the unique values in ascending order assuming they are integers
            sorted_unique_values = sorted(unique_values, key=lambda x: (int(x.split('=')[1]) if x != '' else float('inf')))
            container = st.container()
            # Checkbox to exclude entire question
            if container.checkbox(f"Exclude entire Question: {col}", key=f"exclude_{col}"):
                drop_cols.append(col)
                

            container = st.container()
            all_mappings = {}
            drop_vals = []  # To hold FlowNo values to drop

            for val in sorted_unique_values:
                if pd.notna(val):
                    # Checkbox to exclude specific FlowNo
                    if container.checkbox(f"Exclude FlowNo '{val}'", key=f"exclude_{col}_{val}"):
                        drop_vals.append(val)
                        continue

                    readable_val = container.text_input(f"Rename '{val}' to:", value="", key=f"{col}_{val}")
                    if readable_val:
                        all_mappings[val] = readable_val

            # Remove the excluded FlowNo values from mappings
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
    run2()
