import re

def decode_keypresses(df, qa_dict):
    """Decode keypresses in DataFrame columns based on QA dictionary."""
    for col in df.columns:
        match = re.match(r"FlowNo_(\d+)", col)
        if match:
            question_number = int(match.group(1))
            q_key = f"Q{question_number}"
            if q_key in qa_dict:
                # Create a mapping for this question's answers
                # Assuming 'FlowNo_n=m' where 'm' corresponds to the index of answers in qa_dict
                answer_mapping = {str(i): answer for i, answer in enumerate(qa_dict[q_key]['answers'], start=1)}
                # Apply mapping to the column for decoding
                def decode_value(x):
                    # Extract the answer index from the value
                    answer_index = x.split('=')[-1] if '=' in x else x
                    # Return the readable answer if the index is in the mapping, else return x
                    return answer_mapping.get(answer_index, x)
                df[col] = df[col].apply(decode_value)
    return df
