import streamlit as st
from PIL import Image
import json

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

# Function to parse questions and answers from the uploaded JSON data
def parse_questions_and_answers(json_data):
    """
    Parses the uploaded JSON data to extract questions and their corresponding answers.
    Expected JSON format is a dictionary with keys as 'Q{question_number}' and values are dictionaries
    containing the question text and a dictionary of its answers.
    """
    questions_and_answers = {}
    for q_key, q_value in json_data.items():
        question_text = q_value['question']
        answers = [answer for _, answer in q_value['answers'].items()]
        questions_and_answers[q_key] = {'question': question_text, 'answers': answers}
    return questions_and_answers

def run1():
    st.title('Questionnaire Definer🎡')
    
    st.markdown("### Upload Script Files (.txt,.json format)")
    
    # Check if 'qa_dict' is already in session state, otherwise initialize it
    if 'qa_dict' not in st.session_state:
        st.session_state['qa_dict'] = {}

    # File uploader to allow users to upload a JSON file with scripts
    uploaded_file = st.file_uploader("Choose a txt with formatting or json with flow-mapping file", type=['json', 'txt'])
    if uploaded_file is not None:
        # Reading the uploaded file content
        file_contents = uploaded_file.getvalue().decode("utf-8")
        try:
            # Assuming the uploaded file is JSON
            json_data = json.loads(file_contents)
            st.session_state['qa_dict'] = parse_questions_and_answers(json_data)
            st.success("Questions and answers parsed successfully.✨")
        except json.JSONDecodeError:
            st.error("Error decoding JSON. Please ensure the file is a valid JSON format.")
    else:
        # Optional: Inform the user to upload a file
        st.info("Please upload a file to parse questions and their answers.")
    
    # Remaining code for displaying questions and potentially renaming columns goes here
    st.markdown("## Preview of questions and their answers.")

    # Use an expander for the entire preview section
    with st.expander("Click to view", expanded=False):  # You can set expanded=True to have it open by default
        # Check if there are any questions and answers to display
        if st.session_state.get('qa_dict', None):
            for q_key, q_info in st.session_state['qa_dict'].items():
                st.subheader(f"{q_key}: {q_info['question']}")
                for answer in q_info['answers']:
                    st.write(f"- {answer}")
        else:
            st.write("No questions and answers to display. Please upload a file.")

    if 'cleaned_data' in st.session_state:
        cleaned_data = st.session_state['cleaned_data']
        
        # Assuming qa_dict is loaded into the session state as well
        st.session_state.get('qa_dict', {})
    
        # Create a two-column layout
        col1, col2 = st.columns(2)

        with col1:
            st.write("Rename Columns:")
            new_column_names = []
            for idx, col in enumerate(cleaned_data.columns):
                if idx == 0:
                    # Reserve Q0 for a specific column like "phonenum"
                    default_value = "phonenum"
                else:
                    # Use qa_dict from st.session_state to get the default value for the text input
                    # Adjusted to ensure questions start from Q1 for the first question, respecting the offset
                    default_value = st.session_state['qa_dict'].get(f"Q{idx}", {}).get('question', col)
                new_name = st.text_input(f"Q{idx}:", value=default_value, key=f"new_name_{idx}")
                new_column_names.append(new_name)

        with col2:
            st.write(" ")  # Just to align with the left column

        if st.button("Apply New Column Names"):
            updated_df = rename_columns(cleaned_data, new_column_names)
            st.session_state['renamed_data'] = updated_df  # Save the DataFrame with renamed columns
            st.write("DataFrame with Renamed Columns:")
            st.dataframe(updated_df.head())

    else:
        st.error("No cleaned data found. Please go back to the previous step and process your data first.")

if __name__ == "__main__":
    run1()
