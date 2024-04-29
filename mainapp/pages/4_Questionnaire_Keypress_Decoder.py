import streamlit as st
import pandas as pd
import json
from io import StringIO

# Define the JSON mapping as a Python dictionary (or load it from a file)
questionnaire_mapping = json.loads("""
{
    "Did you vote in the Batu Pahat Parliament?": {"0": "Yes", "1": "No"},
    "Ethnicity": {"0": "Malay", "1": "Chinese", "2": "Indian", "3": "Others"},
    "How do you feel about the news? What is your sentiment towards the cancellation of the Batu Pahat factory license that made 'Allah' stockings?": {
        "0": "5) Very Positive", "1": "4) Positive", "2": "3) Neutral", "3": "2) Negative", "4": "1) Very Negative"
    },
    ...
}
""")

def apply_mappings(data, mappings):
    """ Applies mappings to the data based on the JSON configuration. """
    for column in data.columns:
        if column.startswith("FlowNo_"):
            question_index = int(column.split('_')[1]) - 2  # Assuming FlowNo_2 corresponds to the first question
            question = list(mappings.keys())[question_index]
            answer_mapping = mappings[question]
            data[column] = data[column].map(lambda x: answer_mapping.get(str(int(x)), "") if pd.notna(x) else "")

    return data

def run_app():
    st.title('IVR Survey Data Decoder')
    st.markdown("### Upload your CSV data")

    uploaded_data_file = st.file_uploader("Choose a CSV file", type=['csv'])
    if uploaded_data_file is not None:
        data = pd.read_csv(uploaded_data_file)
        
        st.markdown("### Original Data Preview")
        st.dataframe(data.head())

        if st.button("Decode Data"):
            decoded_data = apply_mappings(data, questionnaire_mapping)
            
            st.markdown("### Decoded Data Preview")
            st.dataframe(decoded_data.head())

            # Optional: Providing a download link for the decoded data
            csv = decoded_data.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download decoded data as CSV",
                data=csv,
                file_name='decoded_data.csv',
                mime='text/csv',
            )

if __name__ == "__main__":
    run_app()
