import pandas as pd
import re

def decode_keypresses(df, qa_dict):
    """Decode keypresses in DataFrame columns based on QA dictionary."""
    for col in df.columns[1:-1]:  # Skip the first and last columns as they don't contain FlowNo data
        col_str = str(col)  # Ensure column name is a string
        match = re.match(r"FlowNo_(\d+)", col_str)
        if match:
            question_number = int(match.group(1))
            q_key = f"Q{question_number}"
            if q_key in qa_dict:
                answer_mapping = {str(i): answer for i, answer in enumerate(qa_dict[q_key]['answers'], start=1)}
                
                def decode_value(x):
                    x_str = str(x)  # Convert the value to string to safely use regex (and handle NaNs correctly)
                    if pd.isnull(x):
                        return x  # Optionally return NaN without changes
                    answer_index = re.sub('[^a-zA-Z]', '', x_str.split('=')[-1] if '=' in x_str else x_str)
                    return answer_mapping.get(answer_index, x_str)
                
                df[col] = df[col].apply(decode_value)
    return df


if __name__ == "__main__":
    decode_keypresses()

