import streamlit as st
import json
import pandas as pd
import re

# Utility functions
def parse_questions_and_answers(json_data):
    """Parse questions and answers from JSON data."""
    questions_and_answers = {}
    for q_key, q_value in json_data.items():
        question_text = q_value['question']
        answers = {k: v for k, v in q_value['answers'].items()}
        questions_and_answers[q_key] = {'question': question_text, 'answers': answers}
    return questions_and_answers

def parse_text_to_json(text_content):
    """Parse structured text content into a JSON-like dictionary."""
    data = {}
    question_re = re.compile(r'^(\d+)\.\s*(.*)')  # Question regex
    answer_re = re.compile(r'^\s*-\s*(.*)')  # Answer regex
    current_question = ""

    for line in text_content.splitlines():
        question_match = question_re.match(line)
        answer_match = answer_re.match(line)

        if question_match:
            q_number, q_text = question_match.groups()
            current_question = f"Q{q_number}"
            data[current_question] = {"question": q_text, "answers": {}}
        elif answer_match and current_question:
            answer_text = answer_match.groups()[0]
            flow_no = len(data[current_question]["answers"]) + 1
            flow_no_key = f"FlowNo_{int(q_number)}={flow_no}"
            data[current_question]["answers"][flow_no_key] = answer_text

    return data

def custom_sort(col):
    """Sort column names based on question and flow numbers."""
    col_str = str(col)  # Ensure the column name is a string
    match = re.match(r"FlowNo_(\d+)=*(\d*)", col_str)
    if match:
        question_num = int(match.group(1))
        flow_no = int(match.group(2)) if match.group(2) else 0
        return (question_num, flow_no)
    else:
        return (float('inf'), 0)

# Initialize session states
if 'cleaned_data' not in st.session_state:
    st.session_state['cleaned_data'] = pd.DataFrame(index=range(0))
if 'qa_dict' not in st.session_state:
    st.session_state['qa_dict'] = {}
if 'renamed_data' not in st.session_state:
    st.session_state['renamed_data'] = pd.DataFrame(index=range(0))

# Title and File Upload Section
st.title('Questionnaire Definer & Keypress Decoder')
st.markdown("### Upload Script Files (.txt, .json format)")

uploaded_file = st.file_uploader("Choose a .txt with formatting or .json with flow-mapping file", type=['txt', 'json'])
file_parsed = False  # Track if a file has been parsed

# Parse Uploaded Files
if uploaded_file is not None:
    file_contents = uploaded_file.getvalue().decode("utf-8")
    
    try:
        # Try loading as JSON first
        flow_no_mappings = json.loads(file_contents)
        parsed_data = parse_questions_and_answers(flow_no_mappings)
        st.session_state['qa_dict'] = parsed_data
        st.success("JSON questions and answers parsed successfully. ✨")
        file_parsed = True
    except json.JSONDecodeError:
        # If JSON decoding fails, attempt parsing as plain text
        parsed_data = parse_text_to_json(file_contents)
        st.session_state['qa_dict'] = parsed_data
        st.success("Text questions and answers parsed successfully. ✨")
        file_parsed = True

# Prepare Keypress Decode Mappings
simple_mappings = {k: v for question in st.session_state['qa_dict'].values() for k, v in question["answers"].items()}
question_mappings = {q_key: q_data["question"] for q_key, q_data in st.session_state['qa_dict'].items()}
keypress_mappings = {}
drop_cols = []
excluded_flow_nos = {}

# Rename Columns in DataFrame
if 'cleaned_data' in st.session_state:
    cleaned_data = st.session_state['cleaned_data']
    
    # Automatically rename column `Q1` with `0` as `phonenum`
    if 'Q1' in cleaned_data.columns and '0' in cleaned_data['Q1'].values:
        cleaned_data.rename(columns={'Q1': 'phonenum'}, inplace=True)

    renamed_data = cleaned_data.rename(columns=simple_mappings)
    
    # Rename column headers based on question mappings
    for col in renamed_data.columns:
        if col in question_mappings:
            renamed_data.rename(columns={col: question_mappings[col]}, inplace=True)

    sorted_columns = sorted(renamed_data.columns, key=custom_sort)
    renamed_data = renamed_data[sorted_columns]
    st.session_state['renamed_data'] = renamed_data
    st.write("Preview of Renamed Column Data:")
    st.dataframe(renamed_data.head())

    question_columns = renamed_data.columns[:-1]  # Exclude the last column (e.g., phonenum)

    for i, col in enumerate(question_columns, start=1):
        st.subheader(f"Q{i}: {col}")
        unique_values = [val for val in renamed_data[col].unique() if pd.notna(val)]
        sorted_unique_values = sorted(unique_values, key=lambda x: int(x.split('=')[1]) if '=' in x and x.split('=')[1] else float('inf'))
        
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

    st.write("Final Mappings:", keypress_mappings)

else:
    st.warning("No cleaned data available for renaming.")
