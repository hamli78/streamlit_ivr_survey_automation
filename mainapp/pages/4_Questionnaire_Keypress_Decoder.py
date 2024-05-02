import streamlit as st
import pandas as pd
import re
import json

# Function to parse the text file
def parse_text_to_json(text_content):
    """
    Converts structured text content into a JSON-like dictionary, parsing questions and their answers.

    Parameters:
    - text_content (str): Text content containing questions and answers in a structured format.

    Returns:
    - dict: A dictionary representing the parsed content with questions as keys and their details (question text and answers) as values.
    """
    data = {}
    question_re = re.compile(r'^(\d+)\.\s*(.*)')  # Adjusted to allow optional spaces after the period
    answer_re = re.compile(r'^\s*-\s*(.*)')  # Adjusted to allow optional spaces around the dash

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
            flow_no_key = f"FlowNo_{int(q_number)+1}={flow_no}"
            data[current_question]["answers"][flow_no_key] = answer_text

    return data

    # Convert the parsed data to a flat dictionary for mapping
    flat_data = {}
    for q_key, q_info in data.items():
        q_num = int(q_key[1:])
        for a_key, a_val in q_info['answers'].items():
            flat_data[f'FlowNo_{q_num}={a_key}'] = a_val

    return flat_data

# Function to map the answers to the data
def map_flowno_to_text(df, qna_mapping):
    for col in df.columns:
        if col.startswith('FlowNo_'):
            # Strip the 'FlowNo_' prefix and parse the index
            index = int(col.split('_')[1].split('=')[0])
            q_text = qna_mapping.get(f'Q{index}', {}).get('question', f'Q{index}')
            a_mapping = {int(k.split('=')[1]): v for k, v in qna_mapping.get(f'Q{index}', {}).get('answers', {}).items()}
            df = df.rename(columns={col: q_text})
            df[q_text] = df[q_text].map(a_mapping)
    return df

# Streamlit App
def main():
    st.title('Survey Data Mapping Tool')

    # File uploader for the text file containing the mapping
    uploaded_text = st.file_uploader('Upload your text file for Q&A mapping', type='txt')
    # File uploader for the CSV file containing the cleaned data
    uploaded_csv = st.file_uploader('Upload your CSV file for cleaned data', type='csv')

    if uploaded_text and uploaded_csv:
        # Read and process the text file
        text_content = uploaded_text.getvalue().decode('utf-8')
        qna_mapping = parse_text_to_json(text_content)

        # Read the CSV file and process it
        df_cleaned_data = pd.read_csv(uploaded_csv)
        df_mapped_data = map_flowno_to_text(df_cleaned_data, qna_mapping)

        # Display the dataframe
        st.write('Mapped Data', df_mapped_data)

# Run the Streamlit app
if __name__ == '__main__':
    main()
