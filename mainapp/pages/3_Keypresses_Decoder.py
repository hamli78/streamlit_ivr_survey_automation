import streamlit as st
import pandas as pd
import json
import re
from io import StringIO

# Set up the page configuration and CSS for dark mode
st.set_page_config(page_title='IVR Data Cleaner 🧮', layout="wide", initial_sidebar_state="expanded")
st.markdown("<style>body { color: #fff; background-color: #111; } </style>", unsafe_allow_html=True)

def parse_questionnaire(content):
    """ Parses the questionnaire using regex to find questions and answers. """
    data = {}
    question_re = re.compile(r'^(\d+)\.\s*(.*)')  # Question number and text
    answer_re = re.compile(r'^\s*-\s*(.*)')  # Answer options

    current_question = None

    for line in content.split('\n'):
        line = line.strip()
        if question_match := question_re.match(line):
            q_num, q_text = question_match.groups()
            current_question = q_text
            data[current_question] = []
        elif answer_match := answer_re.match(line):
            if current_question:
                data[current_question].append(answer_match.group(1))

    return data

def load_mappings(file_content, file_type):
    """ Load mappings from a JSON file or parse from text using regex. """
    if file_type == "application/json":
        return json.loads(file_content)
    else:
        return parse_questionnaire(file_content)

def run_app():
    st.title('IVR Survey Automation Tool')

    # Allow the user to upload a JSON or TXT file with the questionnaire mapping
    uploaded_mapping_file = st.file_uploader("Upload a JSON or TXT file with the mapping", type=['txt', 'json'])
    if uploaded_mapping_file is not None:
        file_content = uploaded_mapping_file.getvalue().decode("utf-8")
        flow_no_mappings = load_mappings(file_content, uploaded_mapping_file.type)
        st.success("Mappings loaded successfully!")
        st.json(flow_no_mappings)

        # Now upload the IVR data file
        uploaded_data_file = st.file_uploader("Now, upload your IVR Data File (CSV format)", type=['csv'])
        if uploaded_data_file is not None:
            data = pd.read_csv(uploaded_data_file)
            st.markdown("### Original Data Preview")
            st.dataframe(data.head())

            if st.button("Decode Data"):
                # Apply the mappings to the DataFrame
                for column in data.columns:
                    if column.startswith("FlowNo_"):
                        question_key = column.split('=')[0]
                        data[column] = data[column].apply(lambda x: flow_no_mappings.get(question_key, {}).get(str(int(x)), x) if pd.notna(x) else x)

                st.markdown("### Decoded Data Preview")
                st.dataframe(data.head())

                # Provide a download button for the decoded CSV
                csv = data.to_csv(index=False).encode('utf-8')
                st.download_button("Download decoded data as CSV", csv, "decoded_data.csv", "text/csv")

if __name__ == "__main__":
    run_app()
