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

