import streamlit as st
from PIL import Image
import pandas as pd
from modules.keypress_decoder_utils_page3 import custom_sort, classify_income, drop_duplicates_from_dataframe

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
    st.error("Please upload the file in the initial step and parse the data.")
    st.stop()

def run():
    if 'renamed_data' in st.session_state:
        renamed_data = st.session_state['renamed_data']

        if 'keypress_mappings' not in st.session_state:
            st.session_state['keypress_mappings'] = {}

        question_columns = renamed_data.columns[1:-1]  # Assuming the first and last columns are not questions

        for i, col in enumerate(question_columns, start=1):
            unique_values = [val for val in renamed_data[col].unique() if pd.notna(val)]
            for val in unique_values:
                unique_key = f"{col}_{val}"

                if unique_key not in st.session_state['keypress_mappings']:
                    st.session_state['keypress_mappings'][unique_key] = val  # Preserving initial mapping

                readable_val = st.text_input(f"Rename '{val}' to:", value=st.session_state['keypress_mappings'][unique_key], key=unique_key)
                st.session_state['keypress_mappings'][unique_key] = readable_val

        if st.button("Decode Keypresses"):
            for col in question_columns:
                if col in renamed_data.columns:
                    renamed_data[col] = renamed_data[col].map(lambda val: st.session_state['keypress_mappings'].get(f"{col}_{val}", val))
            st.session_state['decoded_data'] = renamed_data
            st.dataframe(renamed_data.head())

    else:
        st.error("No renamed data found. Please go back to the previous step and rename your data first.")

if __name__ == "__main__":
    run()
