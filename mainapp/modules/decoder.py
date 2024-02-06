import re

def decode_keypresses(df, qa_dict):
    """Decode keypresses in DataFrame columns based on QA dictionary."""
    for col in df.columns:
        # Identify columns that match the FlowNo pattern
        match = re.match(r"FlowNo_(\d+)", col)
        if match:
            q_number = int(match.group(1))  # Extract question number from column name
            q_key = f"Q{q_number}"
            if q_key in qa_dict:
                # Create a mapping for this question's answers, assuming 'FlowNo_n=m' where m is the answer index
                answer_mapping = {str(i): answer for i, answer in enumerate(qa_dict[q_key]['answers'], start=1)}
                # Apply mapping to decode the column values
                df[col] = df[col].apply(lambda x: answer_mapping.get(x.split('=')[-1], x) if '=' in x else x)
    return df
