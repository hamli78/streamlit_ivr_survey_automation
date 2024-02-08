import streamlit as st
from PIL import Image
from datetime import datetime
import pandas as pd
import re  # For regex operations
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

# Call the function to apply the dark mode CSS
set_dark_mode_css()

def custom_sort(col):
    # Improved regex to capture question and flow numbers accurately
    match = re.match(r"FlowNo_(\d+)=*(\d*)", col)
    if match:
        question_num = int(match.group(1))  # Question number
        flow_no = int(match.group(2)) if match.group(2) else 0  # Flow number, default to 0 if not present
        return (question_num, flow_no) 
    else:
        return (float('inf'), 0)

# Add a file uploader at the beginning of your app
uploaded_file = st.file_uploader("Upload JSON File with FlowNo Mappings", type=['json', 'txt'])

# Initialize a variable to hold the mappings
flow_no_mappings = {}

# Check if a file is uploaded
if uploaded_file is not None:
    # Parse the JSON file
    try:
        # Read the file and load it as JSON
        flow_no_mappings = json.load(uploaded_file)
    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON: {e}")

# Flatten the JSON structure to simplify the mapping access
simple_mappings = {k: v for question in flow_no_mappings.values() for k, v in question["answers"].items()}
for q_key, q_data in flow_no_mappings.items():
    for answer_key, answer_value in q_data["answers"].items():
        simple_mappings[answer_key] = answer_value

def run():
    st.title('Keypresses Decoder')

    if 'renamed_data' in st.session_state:
        renamed_data = st.session_state['renamed_data']
        
        # Sort columns based on custom criteria
        sorted_columns = sorted(renamed_data.columns, key=custom_sort)
        renamed_data = renamed_data[sorted_columns]
        
        st.write("Preview of Renamed Data:")
        st.dataframe(renamed_data.head())

        keypress_mappings = {}
        drop_cols = []
        excluded_flow_nos = {}  # Initialize here for the whole session

        # Extract the relevant columns (excluding the first and last non-question columns).
        question_columns = renamed_data.columns[1:-1]

        for i, col in enumerate(question_columns, start=1):
            st.subheader(f"Q{i}: {col}")
            unique_values = renamed_data[col].unique()
            sorted_unique_values = sorted(unique_values, key=lambda x: (int(x.split('=')[1]) if x != '' else float('inf')))
            
            # Checkbox to exclude entire question
            if st.checkbox(f"Exclude entire Question: {col}", key=f"exclude_{col}"):
                drop_cols.append(col)
                continue
            
            all_mappings = {}
            excluded_flow_nos[col] = []

            for idx, val in enumerate(sorted_unique_values):
                if pd.notna(val):
                    autofill_value = simple_mappings.get(val, "")
                    unique_key = f"{col}_{val}_{idx}"
                    
                    # Checkbox to decide whether to exclude this specific FlowNo value
                    if st.checkbox(f"Exclude '{val}'", key=f"exclude_{unique_key}"):
                        excluded_flow_nos[col].append(val)
                        continue
                    
                    readable_val = st.text_input(f"Rename '{val}' to:", value=autofill_value, key=unique_key)
                    if readable_val:
                        all_mappings[val] = readable_val

            if all_mappings:
                keypress_mappings[col] = all_mappings

        if st.button("Decode Keypresses"):
            # Drop entire questions if needed
            if drop_cols:
                renamed_data.drop(columns=drop_cols, inplace=True)

            # Apply mappings and exclude specific FlowNo values
            for col, col_mappings in keypress_mappings.items():
                if col in renamed_data.columns:  # Ensure column exists
                    renamed_data[col] = renamed_data[col].map(col_mappings).fillna(renamed_data[col])
                    if col in excluded_flow_nos:
                        for val_to_exclude in excluded_flow_nos[col]:
                            renamed_data = renamed_data[renamed_data[col] != val_to_exclude]

            st.session_state['decoded_data'] = renamed_data  # Save updated DataFrame to session state
            
            # Display updated DataFrame and other information...
            
            st.write("Preview of Decoded Data:")
            st.dataframe(renamed_data)
            
            # Display IVR length and shape
            st.write(f'IVR Length: {len(renamed_data)} rows')
            st.write(renamed_data.shape)

            # Current date for reporting
            today = datetime.now()
            st.write(f'IVR count by Set as of {today.strftime("%d-%m-%Y").replace("-0", "-")}')
            st.write(renamed_data['Set'].value_counts())  # Replace 'Set' with the actual column name for 'Set' data

            # Check for null values before dropping
            st.write(f'Before dropping: {len(renamed_data)} rows')
            renamed_data.dropna(inplace=True)
            st.write(f'After dropping: {len(renamed_data)} rows')
            st.write(f'Preview of Total of Null Values per Column:')
            st.write(renamed_data.isnull().sum())

            # Sanity check
            for col in renamed_data.columns:
                st.write(f"Sanity check for {col}:")
                st.write(renamed_data[col].value_counts(normalize=True))
                st.write("\n")
                
            st.write("Preview of Decoded Data:")
            st.dataframe(renamed_data)

            # CSV Download
            formatted_date = datetime.now().strftime("%Y%m%d")
            default_filename = f'IVR_Petaling_Jaya_Survey2023_Decoded_Data_v{formatted_date}.csv'
            output_filename = st.text_input("Edit the filename for download", value=default_filename)
            if not output_filename.lower().endswith('.csv'):
                output_filename += '.csv'

            data_as_csv = renamed_data.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Decoded Data as CSV",
                data=data_as_csv,
                file_name=output_filename,
                mime='text/csv'
            )

    else:
        st.error("No renamed data found. Please go back to the previous step and rename your data first.")

if __name__ == "__main__":
    run()
