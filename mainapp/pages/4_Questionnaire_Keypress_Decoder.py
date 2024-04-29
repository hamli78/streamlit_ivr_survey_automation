import streamlit as st
import pandas as pd
import json
import re

# Set up the page configuration and CSS for dark mode
st.set_page_config(page_title='IVR Data Decoder', layout="wide", initial_sidebar_state="expanded")
st.markdown("<style>body { color: #fff; background-color: #111; }</style>", unsafe_allow_html=True)

def parse_text_to_json(text_content):
    """ Converts structured text into a JSON-like dictionary. """
    data = {}
    question_re = re.compile(r'^(\d+)\.\s*(.*)')
    answer_re = re.compile(r'^\s*-\s*(.*)')

    current_question = None
    for line in text_content.splitlines():
        question_match = question_re.match(line)
        answer_match = answer_re.match(line)

        if question_match:
            q_number, q_text = question_match.groups()
            current_question = f"Q{q_number}"
            data[current_question] = {"question": q_text, "answers": {}}
        elif answer_match and current_question:
            answer_text = answer_match.group(1)
            flow_no = len(data[current_question]["answers"]) + 1
            flow_no_key = f"FlowNo_{int(q_number) + 1}={flow_no}"
            data[current_question]["answers"][flow_no_key] = answer_text

    return data

def flatten_json_structure(flow_no_mappings):
    """ Flatten JSON structure to simplify the mapping access. """
    simple_mappings = {}
    for q_key, q_data in flow_no_mappings.items():
        for answer_key, answer_value in q_data["answers"].items():
            simple_mappings[answer_key] = answer_value
    return simple_mappings

def custom_sort(col):
    """ Custom sort function to sort DataFrame columns based on FlowNo keys. """
    match = re.match(r"FlowNo_(\d+)=(\d+)", col)
    return (int(match.group(1)), int(match.group(2))) if match else (float('inf'), 0)

def classify_income(income):
    """ Classify income into categories based on defined ranges. """
    if income <= 4850:
        return 'B40'
    elif income <= 10960:
        return 'M40'
    elif income > 10960:
        return 'T20'
    return 'Unknown'

def process_file_content(file_type, file_content):
    """ Process the content of the uploaded file. """
    if file_type == "application/json":
        return json.loads(file_content)
    else:
        return parse_text_to_json(file_content)

def run_app():
    st.title('IVR Survey Data Decoder')
    
    # File uploader for mapping configuration
    uploaded_file = st.file_uploader("Upload a JSON or TXT file with the mapping", type=['txt', 'json'])
    if uploaded_file is not None:
        mappings, message, error = process_file_content(uploaded_file.type, uploaded_file.getvalue().decode("utf-8"))
        if error:
            st.error(error)
        else:
            st.success(message)
            flattened_mappings = flatten_json_structure(mappings)

            # File uploader for IVR data
            data_file = st.file_uploader("Upload your IVR Data File (CSV format)", type=['csv'])
            if data_file is not None:
                data = pd.read_csv(data_file)
                st.write("Original Data Preview:", data.head())

                if st.button("Decode Data"):
                    # Apply mappings to the DataFrame
                    for col in data.columns:
                        if "FlowNo_" in col:
                            data[col] = data[col].apply(lambda x: flattened_mappings.get(f"{col}={int(x)}", x))
                    
                    # Optionally classify income
                    if 'IncomeRange' in data.columns:
                        data['IncomeClass'] = data['IncomeRange'].apply(classify_income)

                    st.write("Decoded Data Preview:", data.head())
                    csv = data.to_csv(index=False).encode('utf-8')
                    st.download_button("Download decoded data as CSV", csv, "decoded_data.csv", "text/csv")

if __name__ == "__main__":
    run_app()
