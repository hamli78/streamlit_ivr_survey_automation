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
import streamlit as st
import re

# Function to rename columns based on user input
def rename_columns(df, new_column_names):
    mapping = {old: new for old, new in zip(df.columns, new_column_names) if new}
    return df.rename(columns=mapping, inplace=False)

# Function to parse questions from the uploaded .txt file
def parse_questions(file_contents):
    """
    Parses the uploaded .txt file to extract questions.
    Expected file format:
        1. Question text
        2. Question text
        ...
    Returns a dictionary where keys are 'Q1', 'Q2', ... and values are the corresponding questions.
    """
    questions = {}
    # Adjusting the logic to match your file format and expectations
    for line in file_contents.split('\n'):
        match = re.match(r"(\d+)\.\s*(.*)", line)
        if match:
            question_number, question_text = match.groups()
            questions[f"Q{int(question_number)}"] = question_text.strip()  # Ensure numbering matches user expectation
    return questions

def run():
    st.title('Questionnaire Definer')

    # File uploader to allow users to upload a .txt file with scripts
    uploaded_file = st.file_uploader("Choose a file", type='txt')
    if uploaded_file is not None:
        # Reading the uploaded file and storing its contents
        file_contents = uploaded_file.getvalue().decode("utf-8")
        questions = parse_questions(file_contents)
    else:
        questions = {}

    if 'cleaned_data' in st.session_state:
        cleaned_data = st.session_state['cleaned_data']
        st.write("Preview of Cleaned Data:")
        st.dataframe(cleaned_data.head())

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
                    # Adjusted to ensure questions start from Q1 for the first question, respecting the offset
                    default_value = questions.get(f"Q{idx}", col)
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
    run()


# import pandas as pd
# import re
# # Function to rename columns based on user input
# def rename_columns(df, new_column_names):
#     mapping = {old: new for old, new in zip(df.columns, new_column_names) if new}
#     df.rename(columns=mapping, inplace=True)
#     return df

# # Function to parse questions and answers from the uploaded .txt file
# def parse_questions(file_contents):
#     questions = {}
#     for line in file_contents.split('\n'):
#         match = re.match(r"(\d+)\.\s*(.*)", line)
#         if match:
#             question_number, question_text = match.groups()
#             questions[f"Q{int(question_number)}"] = question_text.strip()
#     return questions

# # Custom sort for handling FlowNo values in column names
# def custom_sort(col):
#     match = re.match(r"FlowNo_(\d+)=*(\d*)", col)
#     if match:
#         question_num = int(match.group(1))
#         flow_no = int(match.group(2)) if match.group(2) else 0
#         return (question_num, flow_no)
#     return (float('inf'), 0)

# def main():
#     st.title('IVR Data Cleaner 🧮')

#     # File uploader for .txt file containing questions and possible answers
#     uploaded_file = st.file_uploader("Choose a .txt file with questions", type='txt')
#     questions = {}
#     if uploaded_file is not None:
#         file_contents = uploaded_file.getvalue().decode("utf-8")
#         questions = parse_questions(file_contents)

#     # Assuming a DataFrame is already loaded or created for demonstration
#     if 'cleaned_data' not in st.session_state:
#         st.session_state['cleaned_data'] = pd.DataFrame({
#             'Column1': [1, 2, 3],
#             'Column2': [4, 5, 6],
#             'Column3': [7, 8, 9]
#         })

#     cleaned_data = st.session_state['cleaned_data']
#     st.write("Preview of Cleaned Data:")
#     st.dataframe(cleaned_data)

#     if st.button("Load and Rename Columns Based on Questions"):
#         if questions:
#             new_column_names = [questions.get(f"Q{i+1}", f"Column{i+1}") for i in range(len(cleaned_data.columns))]
#             cleaned_data = rename_columns(cleaned_data, new_column_names)
#             st.session_state['renamed_data'] = cleaned_data
#             st.success("Columns renamed successfully based on questions.")
#         else:
#             st.error("Please upload a .txt file with questions to rename columns.")

#     if 'renamed_data' in st.session_state:
#         renamed_data = st.session_state['renamed_data']
#         # Additional processing like custom sorting and handling FlowNo can be done here

#         # Displaying the renamed DataFrame
#         st.write("Preview of Renamed Data:")
#         st.dataframe(renamed_data)

#         # Example to demonstrate further processing, like custom sorting
#         # This would be the place to integrate the decoding keypresses functionality
#         # and any additional data manipulations as required

# if __name__ == "__main__":
#     main()