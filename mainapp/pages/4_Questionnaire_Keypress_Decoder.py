import streamlit as st
from PIL import Image
import json
import pandas as pd
from datetime import datetime
from modules.questionnaire_utils_page2 import parse_questions_and_answers, parse_text_to_json as parse_qa_text_to_json, rename_columns
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
        .stTextInput > div > div > input, .stFileUploader > div > div > button, .stCheckbox > label, .stButton > button {
            color: #ffffff;
            background-color: #111111;
        }
    </style>
    """
    st.markdown(dark_mode_css, unsafe_allow_html=True)

set_dark_mode_css()  # Call the function to apply the dark mode CSS

def run():
    st.title('IVR Data Processor 🚀')

    st.markdown("### Upload Script Files (.txt, .json format)")
    uploaded_file = st.file_uploader("Choose a txt with formatting or json with flow-mapping file", type=['txt', 'json'])

    file_parsed = False  # Track if a file has been parsed
    flow_no_mappings = {}

    if uploaded_file is not None:
        file_contents = uploaded_file.getvalue().decode("utf-8")

        if uploaded_file.type == "application/json":
            try:
                json_data = json.loads(file_contents)
                parsed_data = parse_questions_and_answers(json_data)
                st.session_state['qa_dict'] = parsed_data
                flow_no_mappings = json_data
                st.success("JSON questions and answers parsed successfully.✨")
                file_parsed = True
            except json.JSONDecodeError:
                st.error("Error decoding JSON. Please ensure the file is a valid JSON format.")
        else:  # For text format
            parsed_data = parse_qa_text_to_json(file_contents)
            st.session_state['qa_dict'] = parsed_data
            flow_no_mappings = parse_qa_text_to_json(file_contents)
            st.success("Text questions and answers parsed successfully.✨")
            file_parsed = True

    # Section for manual and auto-filled renaming
    if 'cleaned_data' not in st.session_state:
        st.warning("No cleaned data available for renaming.")
        return  # Ensure we don't proceed further if there's no data to work with
    else:
        cleaned_data = st.session_state['cleaned_data']
        column_names_to_display = [col for col in cleaned_data.columns]  # Placeholder for actual column names

        new_column_names = []
        for idx, default_name in enumerate(column_names_to_display):
            if idx == 0:
                default_value = "phonenum"
            elif idx == len(column_names_to_display) - 1:
                default_value = "Set"
            elif file_parsed:
                question_key = f"Q{idx}"
                default_value = st.session_state['qa_dict'].get(question_key, {}).get('question', default_name)
            else:
                default_value = default_name

            new_name = st.text_input(f"Column {idx+1}: {default_name}", value=default_value, key=f"new_name_{idx}")
            new_column_names.append(new_name)

        if st.button("Apply New Column Names"):
            updated_df = rename_columns(cleaned_data, new_column_names)
            st.session_state['renamed_data'] = updated_df
            st.write("DataFrame with Renamed Columns:")
            st.dataframe(updated_df.head())

            decoded_data = st.session_state['renamed_data']
            decoded_data = drop_duplicates_from_dataframe(decoded_data)

            # Sort columns based on custom criteria
            sorted_columns = sorted(decoded_data.columns, key=custom_sort)
            decoded_data = decoded_data[sorted_columns]

            # Classify income and handle additional calculations
            if 'IncomeRange' in decoded_data.columns:
                income_group = decoded_data['IncomeRange'].apply(classify_income)
                income_range_index = decoded_data.columns.get_loc('IncomeRange')
                decoded_data.insert(income_range_index + 1, 'IncomeGroup', income_group)

            # Display updated DataFrame and other information

            st.write("Preview of Decoded Data:")
            st.dataframe(decoded_data)
            
            decoded_data = drop_duplicates_from_dataframe(decoded_data)

            # Display IVR length and shape
            st.write(f'IVR Length: {len(decoded_data)} rows')
            st.write(decoded_data.shape)

            # Current date for reporting
            today = datetime.now()
            st.write(f'IVR count by Set as of {today.strftime("%d-%m-%Y").replace("-0", "-")}')
            st.write(decoded_data['Set'].value_counts())  # Replace 'Set' with the actual column name for 'Set' data
            
            # Check for null values 
            st.markdown("### Null Values Inspection")
            decoded_data.dropna(inplace=True)
            st.write(f'No. of rows after dropping nulls: {len(decoded_data)} rows')
            st.write(f'Preview of Total of Null Values per Column:')
            st.write(decoded_data.isnull().sum())
            
            st.markdown("### Sanity check for values in each column")
            for col in decoded_data.columns:
                if col != 'phonenum':
                    st.write(decoded_data[col].value_counts(normalize=True))
                    st.write("\n")
            
            st.write("Preview of Decoded Data:")
            st.dataframe(decoded_data)

            # Initialize session state for output_filename if it doesn't already exist
            if 'output_filename' not in st.session_state:
                formatted_date = datetime.now().strftime("%Y%m%d")
                st.session_state['output_filename'] = f'IVR_Decoded_Data_v{formatted_date}.csv'

            # Function to update the filename in session state based on user input
            def update_output_filename():
                if st.session_state.output_filename_input and not st.session_state.output_filename_input.lower().endswith('.csv'):
                    st.session_state.output_filename = st.session_state.output_filename_input + '.csv'
                else:
                    st.session_state.output_filename = st.session_state.output_filename_input

            # User input for editing the filename, tied directly to session state
            st.text_input("Edit the filename for download", value=st.session_state['output_filename'], key='output_filename_input', on_change=update_output_filename)

            # Assuming renamed_data is defined elsewhere and is the data you want to download
            data_as_csv = decoded_data.to_csv(index=False).encode('utf-8')

            # Use the session state for the filename in the download button
            st.download_button(
                label="Download Decoded Data as CSV",
                data=data_as_csv,
                file_name=st.session_state['output_filename'],
                mime='text/csv'
            )

if __name__ == "__main__":
    run()

