import streamlit as st
from PIL import Image
from datetime import datetime
import pandas as pd
import json
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

# Load flow_no_mappings from session state if available
if 'qa_dict' not in st.session_state:
    st.error("Flow number mappings not found in session state. Please upload and parse the JSON file in the first script.")
    st.stop()

def run():
    if 'renamed_data' in st.session_state:
        renamed_data = st.session_state['renamed_data']
        sorted_columns = sorted(renamed_data.columns, key=custom_sort)
        renamed_data = renamed_data[sorted_columns]
        
        st.write("Preview of Renamed Data:")
        st.dataframe(renamed_data.head())

        # Using expander to manage large number of unique values and renaming inputs
        with st.expander("Manage FlowNo and Renaming"):
            for i, col in enumerate(sorted_columns):
                st.subheader(f"Column: {col}")
                unique_values = renamed_data[col].dropna().unique()
                for value in unique_values:
                    if f"{col}_{value}" not in st.session_state:
                        st.session_state[f"{col}_{value}"] = st.session_state['qa_dict'].get(value, value)
                    new_label = st.text_input(f"Rename '{value}' to:", value=st.session_state[f"{col}_{value}"], key=f"{col}_{value}_input")
                    st.session_state[f"{col}_{value}"] = new_label

        # Button to apply all renamings
        if st.button("Apply All Renamings"):
            apply_all_renamings(renamed_data, sorted_columns)

    else:
        st.error("No renamed data found. Please go back to the previous step and rename your data first.")

def apply_all_renamings(data, columns):
    for col in columns:
        mappings = {val: st.session_state[f"{col}_{val}"] for val in data[col].dropna().unique()}
        data[col] = data[col].map(mappings).fillna(data[col])
    st.session_state['decoded_data'] = data  # Save updated DataFrame to session state
    st.success("All changes have been applied to the data.")
    st.write("Preview of Decoded Data:")
    st.dataframe(data.head())

if __name__ == "__main__":
    run()
