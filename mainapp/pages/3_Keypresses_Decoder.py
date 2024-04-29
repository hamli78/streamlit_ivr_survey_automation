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

set_dark_mode_css()

st.title('Keypresses Decoder🔑')

if 'qa_dict' not in st.session_state:
    st.error("Please upload the file in the initial step and parse the data.")
    st.stop()

# Use stored mappings
flow_no_mappings = st.session_state['qa_dict']

st.markdown("### Uploaded Data Summary")
st.json(flow_no_mappings)

def run():
    if 'renamed_data' in st.session_state:
        renamed_data = st.session_state['renamed_data']

        # Sort columns based on custom criteria
        sorted_columns = sorted(renamed_data.columns, key=custom_sort)
        renamed_data = renamed_data[sorted_columns]

        st.write("Preview of Renamed Data:")
        st.dataframe(renamed_data.head())

        if 'keypress_mappings' not in st.session_state:
            st.session_state['keypress_mappings'] = {}

        # Extract the relevant columns (excluding the first and last non-question columns).
        question_columns = renamed_data.columns[1:-1]

        for i, col in enumerate(question_columns, start=1):
            st.subheader(f"Q{i}: {col}")

            unique_values = [val for val in renamed_data[col].unique() if pd.notna(val)]
            sorted_unique_values = sorted(unique_values, key=lambda x: int(x.split('=')[1]) if '=' in x and x.split('=')[1].isdigit() else float('inf'))

            # Checkbox to exclude entire question
            if st.checkbox(f"Drop entire Question {i}", key=f"exclude_{col}"):
                renamed_data.drop(columns=[col], inplace=True)
                continue

            for val in sorted_unique_values:
                unique_key = f"{col}_{val}"

                # Checkbox for excluding specific FlowNo value
                if st.checkbox(f"Drop '{val}'", key=f"exclude_{unique_key}"):
                    renamed_data = renamed_data[renamed_data[col] != val]
                    continue

                # Retrieve or initialize the renaming in session state
                if unique_key not in st.session_state['keypress_mappings']:
                    st.session_state['keypress_mappings'][unique_key] = flow_no_mappings.get(val, val)

                # Ensure that the full key=value is used for renaming
                display_key = f"{col}={val}"
                readable_val = st.text_input(f"Rename '{display_key}' to:", value=st.session_state['keypress_mappings'][unique_key], key=unique_key)
                st.session_state['keypress_mappings'][unique_key] = readable_val  # Save back to session state

        if st.button("Decode Keypresses"):
            for col in question_columns:
                if col in renamed_data.columns:
                    # Apply the renaming from session state
                    renamed_data[col] = renamed_data[col].map(lambda val: st.session_state['keypress_mappings'].get(f"{col}_{val}", val))

            st.session_state['decoded_data'] = renamed_data  # Save updated DataFrame to session state
            st.write("Preview of Decoded Data:")
            st.dataframe(renamed_data.head())

    else:
        st.error("No renamed data found. Please go back to the previous step and rename your data first.")

if __name__ == "__main__":
    run()
