#
import streamlit as st
from PIL import Image
from datetime import datetime
import pandas as pd
import re  # For regex operations
import json
from modules.keypress_decoder_utils_page3 import parse_text_to_json, custom_sort, classify_income, drop_duplicates_from_dataframe


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

st.title('Keypresses Decoder🔑')

st.markdown("### Upload Script OR JSON Files (.txt,.json format)")
# Add a file uploader at the beginning of your app
uploaded_file = st.file_uploader("Choose a txt with formatting or json with flow-mapping file", type=['txt','json'])

# Initialize a variable to hold the mappings
flow_no_mappings = {}

# Check if a file is uploaded
if uploaded_file is not None:
    file_content = uploaded_file.getvalue().decode("utf-8")
    file_type = uploaded_file.type
    st.write("File type detected:", file_type)  # Debug file type
    try:
        if file_type == "application/json":
            flow_no_mappings = json.loads(file_content)
        else:
            # Assuming all other files should be treated as text
            flow_no_mappings = parse_text_to_json(file_content)

        # Debugging flow_no_mappings
        st.write("Debug - Flow No Mappings:", flow_no_mappings)

        if flow_no_mappings:
            st.success("Questions and answers parsed successfully.✨")
        else:
            st.error("Parsed data is empty. Check file content and parsing logic.")
    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
        # Optional: Inform the user to upload a file
        st.info("Please upload a file to parse questions and their answers.")
            


# Flatten the JSON structure to simplify the mapping access
simple_mappings = {k: v for question in flow_no_mappings.values() for k, v in question["answers"].items()}
for q_key, q_data in flow_no_mappings.items():
    for answer_key, answer_value in q_data["answers"].items():
        simple_mappings[answer_key] = answer_value

test_input = "Did you vote in the Petaling Jaya Parliament?\n- Yes\n- No"
test_output = parse_text_to_json(test_input)
st.write("Test output from parse_text_to_json:", test_output)

# Debugging simple_mappings
st.write("Debug - Simple Mappings:", simple_mappings)
        
def run():

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
        
        with st.expander("Show Unique Values for FlowNo"):
                for col in question_columns:
                    if col in renamed_data.columns:  # Ensure the column exists
                        st.write(f"Unique Values in {col} before mapping:", renamed_data[col].unique())
                        
        st.write("P/S : After uploading the file, You can review the Unique FlowNo above and check if got any unique FlowNo that is not in the original Script;(it might be due to the user mispressed the key), or drop questions that you don't want to include(analyze) in the DataFrame. Additionally, you can remove any FlowNo entries that don't exist in the script due to mistaken extra keypress entries made by the call center during the campaign that is not alligned with the original script.")
           
        for i, col in enumerate(question_columns, start=1):
            st.subheader(f"Q{i}: {col}")
            
            unique_values = [val for val in renamed_data[col].unique() if pd.notna(val)]
            # Handle cases where values do not follow the 'key=value' format
            def sort_key(x):
                parts = x.split('=')
                if len(parts) > 1 and parts[1] != '':
                    return int(parts[1])
                else:
                    return float('inf')
                
            sorted_unique_values = sorted(unique_values, key=sort_key)
            
            # Checkbox to exclude entire question using question number instead of column name
            if st.checkbox(f"Drop entire Question {i}", key=f"exclude_{col}"):
                drop_cols.append(col)
                continue
                
            all_mappings = {}
            excluded_flow_nos[col] = []

            for idx, val in enumerate(sorted_unique_values):
                if pd.notna(val):
                    autofill_value = simple_mappings.get(val, "")
                    unique_key = f"{col}_{val}_{idx}"
                    
                    # Checkbox to decide whether to exclude this specific FlowNo value
                    if st.checkbox(f"Drop '{val}'", key=f"exclude_{unique_key}"):
                        excluded_flow_nos[col].append(val)
                        continue
                    
                    readable_val = st.text_input(f"Rename '{val}' to:", value=autofill_value, key=unique_key)
                    if readable_val:
                        all_mappings[val] = readable_val

            if all_mappings:
                keypress_mappings[col] = all_mappings

        if st.button("Decode Keypresses"):
            
            # Use an expander for optional debugging output
            with st.expander("Show keypress mappings"):
                st.write("Applying Debugging Details:", keypress_mappings)
                
            # Drop entire questions if needed
            if drop_cols:
                renamed_data.drop(columns=drop_cols, inplace=True)
                
            # Apply mappings and exclude specific FlowNo values
            for col, col_mappings in keypress_mappings.items():
                if col in renamed_data.columns:  # Ensure column exists
                    
                    # Debugging: Verify mappings are correct just before applying###############
                    # st.write(f"Applying mappings for {col}: {col_mappings}")
                    
                    renamed_data[col] = renamed_data[col].map(col_mappings).fillna(renamed_data[col])
                    if col in excluded_flow_nos:
                        for val_to_exclude in excluded_flow_nos[col]:
                            renamed_data = renamed_data[renamed_data[col] != val_to_exclude]
                            
            # Insert the classify_income function right before the CSV download logic
            if 'IncomeRange' in renamed_data.columns:
                # Classify income and store in a temporary column
                income_group = renamed_data['IncomeRange'].apply(classify_income)
                
                # Find the index of 'IncomeRange' column
                income_range_index = renamed_data.columns.get_loc('IncomeRange')
                
                # Insert 'IncomeGroup' column right after 'IncomeRange' column
                renamed_data.insert(income_range_index + 1, 'IncomeGroup', income_group)
            else:
                st.warning("IncomeRange column not found. Please ensure your data includes this column for income classification.")

            st.session_state['decoded_data'] = renamed_data  # Save updated DataFrame to session state
            
            # Display updated DataFrame and other information

            st.write("Preview of Decoded Data:")
            st.dataframe(renamed_data)
            
            renamed_data = drop_duplicates_from_dataframe(renamed_data)

            # Display IVR length and shape
            st.write(f'IVR Length: {len(renamed_data)} rows')
            st.write(renamed_data.shape)

            # Current date for reporting
            today = datetime.now()
            st.write(f'IVR count by Set as of {today.strftime("%d-%m-%Y").replace("-0", "-")}')
            st.write(renamed_data['Set'].value_counts())  # Replace 'Set' with the actual column name for 'Set' data
            
            # Check for null values 
            st.markdown("### Null Values Inspection")
            renamed_data.dropna(inplace=True)
            st.write(f'No. of rows after dropping nulls: {len(renamed_data)} rows')
            st.write(f'Preview of Total of Null Values per Column:')
            st.write(renamed_data.isnull().sum())
            
            st.markdown("### Sanity check for values in each column")
            for col in renamed_data.columns:
                if col != 'phonenum':
                    st.write(renamed_data[col].value_counts(normalize=True))
                    st.write("\n")
            
            st.write("Preview of Decoded Data:")
            st.dataframe(renamed_data)

            # Initialize session state for output_filename if it doesn't already exist
            if 'output_filename' not in st.session_state:
                formatted_date = datetime.now().strftime("%Y%m%d")
                st.session_state['output_filename'] = f'IVR_Decoded_Data_v{formatted_date}.csv'

            # Function to update the filename in session state based on user input
            def update_output_filename():
                if st.session_state.output_filename_input and not st.session_state.output_filename_input.lower().endswith('.csv'):
                    st.session_state.output_filename = st.session_state.output_filename_input + '.csv'
                else:
                    st.session_state.output_filename = st.session_state.output_filename_input

            # User input for editing the filename, tied directly to session state
            st.text_input("Edit the filename for download", value=st.session_state['output_filename'], key='output_filename_input', on_change=update_output_filename)

            # Assuming renamed_data is defined elsewhere and is the data you want to download
            data_as_csv = renamed_data.to_csv(index=False).encode('utf-8')

            # Use the session state for the filename in the download button
            st.download_button(
                label="Download Decoded Data as CSV",
                data=data_as_csv,
                file_name=st.session_state['output_filename'],
                mime='text/csv'
            )

    else:
        st.error("No renamed data found. Please go back to the previous step and rename your data first.")

if __name__ == "__main__":
    run()
