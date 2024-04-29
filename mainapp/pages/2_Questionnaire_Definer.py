import streamlit as st
from PIL import Image
import json
from modules.questionnaire_utils_page2 import parse_questions_and_answers, parse_text_to_json, rename_columns
import pandas as pd

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
            color: #ffffff;
            background-color: #111111;
        }
        .stTextInput > div > div > input, .stFileUploader > div > div > button {
            color: #ffffff;
            background-color: #111111;
        }
        .stCheckbox > label, .stButton > button {
            color: #ffffff;
        }
    </style>
    """
    st.markdown(dark_mode_css, unsafe_allow_html=True)

set_dark_mode_css()

def run1():
    st.title('Questionnaire Definer🎡')
    st.markdown("### Upload Script Files (.txt, .json format)")

    uploaded_file = st.file_uploader("Choose a txt with formatting or json with flow-mapping file", type=['txt','json'])
    file_parsed = False  # Track if a file has been parsed

    if uploaded_file is not None:
        file_contents = uploaded_file.getvalue().decode("utf-8")

        if uploaded_file.type == "application/json":
            try:
                json_data = json.loads(file_contents)
                parsed_data = parse_questions_and_answers(json_data)
                st.session_state['qa_dict'] = parsed_data
                st.success("JSON questions and answers parsed successfully.✨")
                file_parsed = True
            except json.JSONDecodeError:
                st.error("Error decoding JSON. Please ensure the file is a valid JSON format.")
        else:
            parsed_data = parse_text_to_json(file_contents)
            st.session_state['qa_dict'] = parsed_data
            st.success("Text questions and answers parsed successfully.✨")
            file_parsed = True

    # Section for manual and auto-filled renaming
    st.markdown("## Rename Columns")
    if 'cleaned_data' not in st.session_state:
        st.session_state['cleaned_data'] = pd.DataFrame()  # Placeholder for data
        st.warning("No cleaned data available for renaming.")
    else:
        cleaned_data = st.session_state['cleaned_data']
        if 'renamed_columns' not in st.session_state:
            st.session_state['renamed_columns'] = cleaned_data.columns.tolist()

        for idx, default_name in enumerate(st.session_state['renamed_columns']):
            new_name = st.text_input(f"Column {idx+1}: {default_name}", value=default_name, key=f"new_name_{idx}")
            st.session_state['renamed_columns'][idx] = new_name

        if st.button("Apply New Column Names"):
            updated_df = rename_columns(cleaned_data, st.session_state['renamed_columns'])
            st.session_state['renamed_data'] = updated_df
            st.dataframe(updated_df.head())

if __name__ == "__main__":
    run1()
