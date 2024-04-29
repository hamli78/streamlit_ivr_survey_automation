import streamlit as st
import pandas as pd
import re
from datetime import datetime

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

def run_app():
    st.title('IVR Survey Automation Tool')
    st.markdown("### Upload your Questionnaire Text File")
    
    uploaded_qfile = st.file_uploader("Upload a TXT file with the questionnaire", type=['txt'])
    if uploaded_qfile is not None:
        content = uploaded_qfile.getvalue().decode("utf-8")
        qa_dict = parse_questionnaire(content)
        st.success("Questionnaire parsed successfully!")
        st.json(qa_dict)

    st.markdown("### Now, upload your IVR Data File (CSV format)")
    uploaded_data_file = st.file_uploader("Choose a CSV file", type=['csv'])
    if uploaded_data_file is not None and qa_dict:
        data = pd.read_csv(uploaded_data_file)
        data.columns = data.columns.map(str)  # Ensure column names are strings
        
        st.markdown("### Original Data Preview")
        st.dataframe(data.head())

        if st.button("Map and Rename Columns"):
            # Assume each column in CSV corresponds to a question in the order they appear
            col_mapping = {str(idx + 1): question for idx, question in enumerate(qa_dict.keys())}
            renamed_data = data.rename(columns=col_mapping)

            st.markdown("### Renamed Data Preview")
            st.dataframe(renamed_data.head())

            # Optional: Save the renamed DataFrame to session state or perform further processing
            st.session_state['renamed_data'] = renamed_data

if __name__ == "__main__":
    run_app()
