import streamlit as st
import pandas as pd
import re

# Function to parse the text file
def parse_text_to_json(text_content):
    data = {}
    question_re = re.compile(r'^(\d+)\.\s*(.*)')
    answer_re = re.compile(r'^\s*-\s*(.*)')

    current_question = 1
    for line in text_content.splitlines():
        question_match = question_re.match(line)
        answer_match = answer_re.match(line)

        if question_match:
            current_question += 1
            data[f'FlowNo_{current_question}='] = float('nan')
        elif answer_match:
            answer_text = answer_match.group(1)
            answer_index = len([k for k in data.keys() if f'FlowNo_{current_question}=' in k])
            data[f'FlowNo_{current_question}={answer_index+1}'] = answer_text

    return data

# Function to map the answers to the data
def map_answers_to_data(df, answers_dict):
    for col in df.columns:
        if 'FlowNo' in col:
            key = col.split('=')[0] + '='
            mapping = {int(k.split('=')[1]): v for k, v in answers_dict.items() if k.startswith(key)}
            df[col] = df[col].map(mapping, na_action='ignore')
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
        answers_dict = parse_text_to_json(text_content)

        # Read the CSV file and process it
        df_cleaned_data = pd.read_csv(uploaded_csv)
        df_mapped_data = map_answers_to_data(df_cleaned_data, answers_dict)

        # Display the dataframe
        st.write('Mapped Data', df_mapped_data)

# Run the Streamlit app
if __name__ == '__main__':
    main()
