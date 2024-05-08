import streamlit as st
from PIL import Image
from datetime import datetime
import json
import pandas as pd
from modules.questionnaire_utils_page2 import parse_questions_and_answers, parse_text_to_json, rename_columns
from modules.keypress_decoder_utils_page3 import custom_sort, classify_income, drop_duplicates_from_dataframe

# Configure the default settings of the page
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

# Initialize session state
if 'cleaned_data' not in st.session_state:
    st.session_state['cleaned_data'] = pd.DataFrame()
if 'qa_dict' not in st.session_state:
    st.session_state['qa_dict'] = {}
if 'renamed_data' not in st.session_state:
    st.session_state['renamed_data'] = pd.DataFrame()
if 'column_checks' not in st.session_state:
    st.session_state['column_checks'] = {}

def combined_page4():
    st.title('Questionnaire Definer & Keypress Decoder 🎡🔑')
    st.markdown("### Upload Script Files (.txt, .json format)")

    uploaded_file = st.file_uploader("Choose a txt with formatting or json with flow-mapping file", type=['txt', 'json'])
    file_parsed = False

    # Parsing questions and answers
    if uploaded_file is not None:
        file_contents = uploaded_file.getvalue().decode("utf-8")

        if uploaded_file.type == "application/json":
            try:
                json_data = json.loads(file_contents)
                parsed_data = parse_questions_and_answers(json_data)
                st.session_state['qa_dict'] = parsed_data
                st.success("JSON questions and answers parsed successfully. ✨")
                file_parsed = True
            except json.JSONDecodeError:
                st.error("Error decoding JSON. Please ensure the file is a valid JSON format.")
        else:
            parsed_data = parse_text_to_json(file_contents)
            st.session_state['qa_dict'] = parsed_data
            st.success("Text questions and answers parsed successfully. ✨")
            file_parsed = True

        # Prepare cleaned data DataFrame based on parsed questions
        flow_no_mappings = st.session_state['qa_dict']
        if not st.session_state['cleaned_data'].empty:
            cleaned_data = st.session_state['cleaned_data']
        else:
            columns = list(flow_no_mappings.keys()) + ['phonenum']
            st.session_state['cleaned_data'] = pd.DataFrame(columns=columns)

    # Rename columns section
    st.markdown("## Rename Columns")
    if 'cleaned_data' not in st.session_state or st.session_state['cleaned_data'].empty:
        st.warning("No cleaned data available for renaming.")
    else:
        cleaned_data = st.session_state['cleaned_data']

        # Automatically rename `Q1` column to `phonenum` if `Q1` contains value `0`
        if 'Q1' in cleaned_data.columns and '0' in cleaned_data['Q1'].values:
            cleaned_data.rename(columns={'Q1': 'phonenum'}, inplace=True)

        # Apply question mappings
        question_mappings = {q_key: q_data['question'] for q_key, q_data in st.session_state['qa_dict'].items()}
        column_names_to_display = [question_mappings.get(col, col) for col in cleaned_data.columns]

        # Manual input for renaming columns
        new_column_names = []
        for idx, default_name in enumerate(column_names_to_display):
            new_name = st.text_input(f"Column {idx + 1}: {cleaned_data.columns[idx]}", value=default_name, key=f"new_name_{idx}")
            new_column_names.append(new_name)

        if st.button("Apply New Column Names"):
            updated_df = rename_columns(cleaned_data, new_column_names)
            st.session_state['renamed_data'] = updated_df
            st.write("Preview of Cleaned Data from Page 1:")
            st.dataframe(updated_df.head())

    # Process Keypress Data
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
                        autofill_value = st.session_state['qa_dict'].get(val, "")
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
                st.markdown("### Decoded Data")
                st.write("Preview of Decoded Data:")
                st.dataframe(renamed_data)

                today = datetime.now()
                st.write(f'IVR count by Set as of {today.strftime("%d-%m-%Y").replace("-0", "-")}')
                st.write(renamed_data['Set'].value_counts())

                renamed_data.dropna(inplace=True)
                st.session_state['renamed_data'] = renamed_data
                st.write(f'No. of rows after dropping nulls: {len(renamed_data)} rows')
                st.write(f'Preview of Total of Null Values per Column:')
                st.write(renamed_data.isnull().sum())

                st.markdown("### Sanity check for values in each column")

                def run_sanity_check(index, col, data):
                    st.write(f"{index}: {col}")
                    value_counts = data[col].value_counts(normalize=True, dropna=False)
                    st.write(value_counts)

                for index, col in enumerate(renamed_data.columns, start=0):
                    if col != 'phonenum':
                        run_sanity_check(index, col, renamed_data)
                        st.session_state['column_checks'][col] = True

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
if __name__ == "__main__":
    combined_page4()
