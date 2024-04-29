import streamlit as st
from PIL import Image
import pandas as pd
from modules.keypress_decoder_utils_page3 import custom_sort

# Configure the default settings of the page.
icon = Image.open('./images/invoke_logo.png')
st.set_page_config(page_title='Keypresses Decoder🔑', layout="wide", page_icon=icon, initial_sidebar_state="expanded")

def set_dark_mode_css():
    dark_mode_css = """
    <style>
        html, body, [class*="View"] {
            color: #ffffff;
            background-color: #111111;
        }
        .stTextInput > div > div > input {
            color: #ffffff;
            background-color: #111111;
        }
        .stCheckbox > label {
            color: #ffffff;
        }
    </style>
    """
    st.markdown(dark_mode_css, unsafe_allow_html=True)

set_dark_mode_css()

st.title('Keypresses Decoder🔑')

if 'qa_dict' not in st.session_state:
    st.error("Please upload the file in the first script and parse the data.")
    st.stop()

# Assuming some DataFrame is already loaded for demonstration
# For example, initializing a placeholder DataFrame if not present
if 'renamed_data' not in st.session_state:
    st.session_state['renamed_data'] = pd.DataFrame({
        'Question1': ['1-Yes', '2-No'],
        'Question2': ['1-Yes', '2-No', '3-Maybe']
    })

def run():
    renamed_data = st.session_state['renamed_data']
    question_columns = renamed_data.columns  # Modify this as needed
    
    st.markdown("## Review and Decode Responses")
    for col in question_columns:
        st.subheader(f"Column: {col}")
        answers = renamed_data[col].unique()
        for answer in answers:
            if f"{col}_{answer}" not in st.session_state:
                st.session_state[f"{col}_{answer}"] = st.session_state['qa_dict'].get(answer, answer)
            new_answer = st.text_input(f"Rename '{answer}' to:", value=st.session_state[f"{col}_{answer}"], key=f"{col}_{answer}_input")
            st.session_state[f"{col}_{answer}"] = new_answer

        if st.button(f"Apply Changes to {col}"):
            apply_changes(col, renamed_data)

def apply_changes(column, data):
    mappings = {val: st.session_state[f"{column}_{val}"] for val in data[column].unique()}
    data[column] = data[column].map(mappings)
    st.session_state['decoded_data'] = data  # Save updated DataFrame to session state
    st.success(f"Changes applied to {column}")

if __name__ == "__main__":
    run()
