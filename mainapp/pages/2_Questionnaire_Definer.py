###Paling baru 9 feb pukul 8s
### perlu tambah feature untuk buat hantar script file
import streamlit as st
from PIL import Image
import json
import re

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

## Call the function to apply the dark mode CSS
set_dark_mode_css()

# Function to rename columns based on user input
def rename_columns(df, new_column_names):
    mapping = {old: new for old, new in zip(df.columns, new_column_names) if new}
    return df.rename(columns=mapping, inplace=False)

def parse_questions_and_answers(json_data):
    questions_and_answers = {}
    for q_key, q_value in json_data.items():
        question_text = q_value['question']
        answers = [answer for _, answer in q_value['answers'].items()]
        questions_and_answers[q_key] = {'question': question_text, 'answers': answers}
    return questions_and_answers

# New function for parsing text content
def parse_text_to_json(text_content):
    data = {}
    question_re = re.compile(r'^(\d+)\.\s+(.*)')
    answer_re = re.compile(r'^\s+-\s+(.*)')

    for line in text_content.splitlines():
        question_match = question_re.match(line)
        answer_match = answer_re.match(line)

        if question_match:
            q_number, q_text = question_match.groups()
            current_question = f"Q{q_number}"
            data[current_question] = {"question": q_text, "answers": {}}
        elif answer_match:
            answer_text = answer_match.groups()[0]
            flow_no = len(data[current_question]["answers"]) + 1
            flow_no_key = f"FlowNo_{int(q_number)+1}={flow_no}"
            data[current_question]["answers"][flow_no_key] = answer_text

    return data

def run1():
    st.title('Questionnaire Definer🎡')
    st.markdown("### Upload Script Files (.txt,.json format)")

    uploaded_file = st.file_uploader("Choose a txt with formatting or json with flow-mapping file", type=['json', 'txt'])
    if uploaded_file is not None:
        file_contents = uploaded_file.getvalue().decode("utf-8")

        if uploaded_file.type == "application/json":
            try:
                json_data = json.loads(file_contents)
                st.session_state['qa_dict'] = parse_questions_and_answers(json_data)
                st.success("JSON questions and answers parsed successfully.✨")
            except json.JSONDecodeError:
                st.error("Error decoding JSON. Please ensure the file is a valid JSON format.")
        else:  # Assume text format
            st.session_state['qa_dict'] = parse_text_to_json(file_contents)
            st.success("Text questions and answers parsed successfully.✨")

    if 'qa_dict' in st.session_state:
        st.markdown("## Preview of questions and their answers.")
        with st.expander("Click to view", expanded=False):
            for q_key, q_info in st.session_state['qa_dict'].items():
                st.subheader(f"{q_key}: {q_info['question']}")
                for answer in q_info['answers'].values():
                    st.write(f"- {answer}")

    # Assuming 'cleaned_data' needs to be prepared or loaded before this step.
    # This code block should be conditioned to only run after both 'cleaned_data' and 'qa_dict' are available.
    if 'cleaned_data' in st.session_state and 'qa_dict' in st.session_state:
        cleaned_data = st.session_state['cleaned_data']

        st.write("Rename Columns:")
        new_column_names = []
        for idx, col in enumerate(cleaned_data.columns):
            default_value = "phonenum" if idx == 0 else st.session_state['qa_dict'].get(f"Q{idx}", {}).get('question', col)
            new_name = st.text_input(f"Column {idx+1} ({col}):", value=default_value, key=f"new_name_{idx}")
            new_column_names.append(new_name)

        if st.button("Apply New Column Names"):
            updated_df = rename_columns(cleaned_data, new_column_names)
            st.session_state['renamed_data'] = updated_df
            st.write("DataFrame with Renamed Columns:")
            st.dataframe(updated_df.head())
    else:
        if 'qa_dict' in st.session_state:  # Show this message only if questions are already loaded
            st.error("No cleaned data found. Please ensure your data is ready for column renaming.")

if __name__ == "__main__":
    run1()