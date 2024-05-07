import streamlit as st
from PIL import Image
from datetime import datetime
import pandas as pd
import json
from modules.keypress_decoder_utils_page3 import parse_text_to_json, custom_sort, classify_income, drop_duplicates_from_dataframe

# Configure the default settings of the page.
icon = Image.open('./images/invoke_logo.png')
st.set_page_config(page_title='IVR Data Cleaner 🧮', layout="wide", page_icon=icon, initial_sidebar_state="expanded")

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
st.markdown("### Upload Script OR JSON Files (.txt, .json format)")
uploaded_file = st.file_uploader("Choose a txt with formatting or json with flow-mapping file", type=['txt', 'json'])

flow_no_mappings = {}

if uploaded_file is not None:
    file_content = uploaded_file.getvalue().decode("utf-8")
    file_type = uploaded_file.type
    st.write("File type detected:", file_type)
    try:
        if file_type == "application/json":
            flow_no_mappings = json.loads(file_content)
        else:
            flow_no_mappings = parse_text_to_json(file_content)
        st.write("Debug - Flow No Mappings:", flow_no_mappings)
        if flow_no_mappings:
            st.success("Questions and answers parsed successfully.✨")
        else:
            st.error("Parsed data is empty. Check file content and parsing logic.")
    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.info("Please upload a file to parse questions and their answers.")

simple_mappings = {k: v for question in flow_no_mappings.values() for k, v in question["answers"].items()}
for q_key, q_data in flow_no_mappings.items():
    for answer_key, answer_value in q_data["answers"].items():
        simple_mappings[answer_key] = answer_value

test_input = "Did you vote in the Petaling Jaya Parliament?\n- Yes\n- No"
test_output = parse_text_to_json(test_input)
st.write("Test output from parse_text_to_json:", test_output)
st.write("Debug - Simple Mappings:", simple_mappings)

if 'renamed_data' not in st.session_state:
    st.session_state['renamed_data'] = pd.DataFrame()

def process_data():
    if 'renamed_data' in st.session_state and not st.session_state['renamed_data'].empty:
        renamed_data = st.session_state['renamed_data']
        
        sorted_columns = sorted(renamed_data.columns, key=custom_sort)
        renamed_data = renamed_data[sorted_columns]
        st.session_state['renamed_data'] = renamed_data
        st.write("Preview of Renamed Column Data:")
        st.dataframe(renamed_data.head())

        keypress_mappings = {}
        drop_cols = []
        excluded_flow_nos = {}

        question_columns = renamed_data.columns[1:-1]
        with st.expander("Show Unique Values for FlowNo"):
            for col in question_columns:
                if col in renamed_data.columns:
                    st.write(f"Unique Values in {col} before mapping:", renamed_data[col].unique())

        for i, col in enumerate(question_columns, start=1):
            st.subheader(f"Q{i}: {col}")
            unique_values = [val for val in renamed_data[col].unique() if pd.notna(val)]
            sorted_unique_values = sorted(unique_values, key=lambda x: int(x.split('=')[1]) if '=' in x and x.split('=')[1] else float('inf'))

            if st.checkbox(f"Drop entire Question {i}", key=f"exclude_{col}"):
                drop_cols.append(col)
                continue

            all_mappings = {}
            excluded_flow_nos[col] = []

            for idx, val in enumerate(sorted_unique_values):
                if pd.notna(val):
                    autofill_value = simple_mappings.get(val, "")
                    unique_key = f"{col}_{val}_{idx}"
                    if st.checkbox(f"Drop '{val}'", key=f"exclude_{unique_key}"):
                        excluded_flow_nos[col].append(val)
                        continue

                    readable_val = st.text_input(f"Rename '{val}' to:", value=autofill_value, key=unique_key)
                    if readable_val:
                        all_mappings[val] = readable_val

            if all_mappings:
                keypress_mappings[col] = all_mappings

        if st.button("Decode Keypresses"):
            if drop_cols:
                renamed_data.drop(columns=drop_cols, inplace=True)
            for col, col_mappings in keypress_mappings.items():
                if col in renamed_data.columns:
                    renamed_data[col] = renamed_data[col].map(col_mappings).fillna(renamed_data[col])
                    for val_to_exclude in excluded_flow_nos.get(col, []):
                        renamed_data = renamed_data[renamed_data[col] != val_to_exclude]

            if 'IncomeRange' in renamed_data.columns:
                income_group = renamed_data['IncomeRange'].apply(classify_income)
                income_range_index = renamed_data.columns.get_loc('IncomeRange')
                renamed_data.insert(income_range_index + 1, 'IncomeGroup', income_group)

            renamed_data = drop_duplicates_from_dataframe(renamed_data)
            st.session_state['renamed_data'] = renamed_data
            st.write("Preview of Decoded Data:")
            st.dataframe(renamed_data)

            today = datetime.now()
            st.write(f'IVR count by Set as of {today.strftime("%d-%m-%Y").replace("-0", "-")}')
            st.write(renamed_data['Set'].value_counts())

            renamed_data.dropna(inplace=True)
            st.write(f'No. of rows after dropping nulls: {len(renamed_data)} rows')
            st.write(f'Preview of Total of Null Values per Column:')
            st.write(renamed_data.isnull().sum())

            st.markdown("### Checking DataFrame content and data types")
            st.write(renamed_data)
            st.write(renamed_data.dtypes)

            st.markdown("### Sanity check for values in each column")
            for col in renamed_data.columns:
                st.write(f"Column: {col}")
                value_counts = renamed_data[col].value_counts(normalize=True, dropna=False)
                st.write(value_counts)
                st.text(f"Unique values in {col}: {renamed_data[col].unique()}")

            formatted_date = datetime.now().strftime("%Y%m%d")
            st.session_state['output_filename'] = f'IVR_Decoded_Data_v{formatted_date}.csv'
            def update_output_filename():
                st.session_state['output_filename'] = st.session_state['output_filename_input'] + '.csv' if not st.session_state['output_filename_input'].lower().endswith('.csv') else st.session_state['output_filename_input']
            st.text_input("Edit the filename for download", value=st.session_state['output_filename'], key='output_filename_input', on_change=update_output_filename)
            data_as_csv = renamed_data.to_csv(index=False).encode('utf-8')
            st.download_button("Download Decoded Data as CSV", data=data_as_csv, file_name=st.session_state['output_filename'], mime='text/csv')
    else:
        st.error("No renamed data found. Please go back to the previous step and rename your data first.")

if __name__ == "__main__":
    process_data()
