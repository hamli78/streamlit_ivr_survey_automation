import streamlit as st
from PIL import Image
import json
from modules.questionnaire_utils_page2 import parse_questions_and_answers, parse_text_to_json

# Configure the default settings of the page.
icon = Image.open('./images/invoke_logo.png')
st.set_page_config(page_title='IVR Data Cleaner 🧮', layout="wide", page_icon=icon, initial_sidebar_state="expanded")

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
    uploaded_file = st.file_uploader("Choose a txt with formatting or json with flow-mapping file", type=['txt', 'json'])

    if uploaded_file is not None and 'qa_dict' not in st.session_state:
        file_contents = uploaded_file.getvalue().decode("utf-8")
        if uploaded_file.type == "application/json":
            try:
                json_data = json.loads(file_contents)
                st.session_state['qa_dict'] = json_data
                st.success("JSON questions and answers parsed successfully.✨")
            except json.JSONDecodeError:
                st.error("Error decoding JSON. Please ensure the file is a valid JSON format.")
        else:
            parsed_data = parse_text_to_json(file_contents)
            st.session_state['qa_dict'] = parsed_data
            st.success("Text questions and answers parsed successfully.✨")

if __name__ == "__main__":
    run1()
