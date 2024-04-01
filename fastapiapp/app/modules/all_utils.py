# I move this to main.py because this is basically main fastapi

# from fastapi import FastAPI, HTTPException, UploadFile, File, Form
# from modules.data_cleaner_utils_page1 import (
#     process_file
# )
# from modules.questionnaire_utils_page2 import (parse_questions_and_answers,
#     rename_columns
# )
# from modules.keypress_decoder_utils_page3 import (parse_text_to_json , custom_sort , classify_income , process_file_content, flatten_json_structure)

# import pandas as pd
# import json

# app = FastAPI()

# @app.post("/utilities/")
# def utilities_endpoint(
#     action: str = Form(...),
#     uploaded_file: UploadFile = File(None),
#     text_content: str = Form(None),
#     json_data: str = Form(None),
#     new_column_names: str = Form(None),
#     income: str = Form(None),  # For classify_income
#     sort_keys: str = Form(None)  # New for custom_sort
# ):  
#     try:
#         if action == "process_file":
#             if not uploaded_file:
#                 raise HTTPException(status_code=400, detail="Uploaded file is required for this action.")
#             df_complete, phonenum_list, total_calls, total_pickup = process_file(uploaded_file.file)
#             return {
#                 "df_complete": df_complete.to_json(orient="records"),
#                 "phonenum_list": phonenum_list.to_json(orient="records"),
#                 "total_calls": total_calls,
#                 "total_pickup": total_pickup
#             }
            
#         # Handling file processing
#         if action == "process_file_content":
#             if not uploaded_file:
#                 raise HTTPException(status_code=400, detail="Uploaded file is required for this action.")
#             processed_data, message, error = process_file_content(uploaded_file)
#             if error:
#                 raise HTTPException(status_code=500, detail=error)
#             return {"processed_data": processed_data, "message": message}
        
#         elif action == "parse_questions_and_answers":
#             if not json_data:
#                 raise HTTPException(status_code=400, detail="JSON data is required for this action.")
#             parsed_data = parse_questions_and_answers(json.loads(json_data))
#             return parsed_data
#         elif action == "parse_text_to_json":
#             if not text_content:
#                 raise HTTPException(status_code=400, detail="Text content is required for this action.")
#             json_data = parse_text_to_json(text_content)
#             return json_data
#         elif action == "rename_columns":
#             if not json_data or not new_column_names:
#                 raise HTTPException(status_code=400, detail="JSON data and new column names are required for this action.")
#             df = pd.DataFrame(json.loads(json_data))
#             updated_df = rename_columns(df, json.loads(new_column_names))
#             return updated_df.to_json(orient="records")
#         elif action == "flatten_json_structure":
#             if not json_data:
#                 raise HTTPException(status_code=400, detail="JSON data is required for this action.")
#             flat_data = flatten_json_structure(json.loads(json_data))
#             return flat_data
        
#         elif action == "classify_income":
#                     if not income:
#                         raise HTTPException(status_code=400, detail="Income data is required for this action.")
#                     income_category = classify_income(income)
#                     return {"income_category": income_category}
                
#         # New action for custom_sort
#         elif action == "custom_sort":
#             if not sort_keys:
#                 raise HTTPException(status_code=400, detail="Sort keys are required for this action.")
#             # Assuming sort_keys is a JSON string representing a list of keys
#             keys = json.loads(sort_keys)
#             if not isinstance(keys, list):
#                 raise HTTPException(status_code=400, detail="Sort keys must be a list.")
#             sorted_keys = sorted(keys, key=lambda x: custom_sort(x))
#             return {"sorted_keys": sorted_keys}

#         else:
#             raise HTTPException(status_code=400, detail="Unsupported action.")

    
#     except Exception as e:
#         # General error handling
#         raise HTTPException(status_code=500, detail=str(e))

# All_Utils
# import pandas as pd
# import numpy as np

# def process_file(uploaded_file):
#     """
#     Process the uploaded CSV file to extract and transform phone number data
#     and user response data for analysis.
    
#     The function performs several steps:
#     - Reads the CSV, skipping the first row and setting column names dynamically.
#     - Drops columns that are entirely NA.
#     - Extracts columns for phone numbers and user responses.
#     - Identifies total number of calls and total pickups.
#     - Filters data to complete responses where a user key press is recorded.
#     - Adds a 'Set' column to indicate data belonging to the IVR set.
#     - Filters for records where the user key press response is exactly 10 characters long.

#     Parameters:
#     - uploaded_file: A file-like object representing the uploaded CSV file.
#                      This object must support file-like operations such as read.

#     Returns:
#     - A tuple containing:
#         - df_complete: A pandas DataFrame of the processed data, with calls that have complete information.
#         - phonenum_list: A pandas DataFrame containing the list of phone numbers that have at least one user key press.
#         - total_calls: The total number of calls (rows) in the uploaded file.
#         - total_pickup: The total number of calls where a user key press was recorded.

#     Note:
#     - The function assumes the uploaded CSV has specific columns of interest, notably 'PhoneNo' and 'UserKeyPress'.
#     - It is assumed that the second row of the CSV provides the column names for the data.
#     """
#     df = pd.read_csv(uploaded_file, skiprows=1, names=range(100), engine='python')
#     df.dropna(axis='columns', how='all', inplace=True)
#     df.columns = df.iloc[0]
#     df_phonenum = df[['PhoneNo']]
#     df_response = df.loc[:, 'UserKeyPress':]
#     df_results = pd.concat([df_phonenum, df_response], axis='columns')
    
#     total_calls = len(df_results)
#     phonenum_recycle = df_results.dropna(subset=['UserKeyPress'])
#     phonenum_list = phonenum_recycle[['PhoneNo']]
    
#     df_complete = df_results.dropna(axis='index')
#     total_pickup = len(df_complete)

#     df_complete.columns = np.arange(len(df_complete.columns))
#     df_complete['Set'] = 'IVR'
#     df_complete = df_complete.loc[:, :'Set']
#     df_complete = df_complete.loc[(df_complete.iloc[:, 2].str.len() == 10)]

#     return df_complete, phonenum_list, total_calls, total_pickup

# import re

# def parse_questions_and_answers(json_data):
#     """
#     Parses questions and their respective answers from a JSON data structure.

#     Parameters:
#     - json_data (dict): A dictionary containing questions as keys and their details (question text and answers) as values.

#     Returns:
#     - dict: A dictionary with question numbers as keys and a sub-dictionary containing the question text and a list of answers.
#     """
#     questions_and_answers = {}
#     for q_key, q_value in json_data.items():
#         question_text = q_value['question']
#         answers = [answer for _, answer in q_value['answers'].items()]
#         questions_and_answers[q_key] = {'question': question_text, 'answers': answers}
#     return questions_and_answers

# def parse_text_to_json(text_content):
#     """
#     Converts structured text content into a JSON-like dictionary, parsing questions and their answers.

#     Parameters:
#     - text_content (str): Text content containing questions and answers in a structured format.

#     Returns:
#     - dict: A dictionary representing the parsed content with questions as keys and their details (question text and answers) as values.
#     """
#     data = {}
#     question_re = re.compile(r'^(\d+)\.\s+(.*)')
#     answer_re = re.compile(r'^\s+-\s+(.*)')
#     current_question = ""

#     for line in text_content.splitlines():
#         question_match = question_re.match(line)
#         answer_match = answer_re.match(line)

#         if question_match:
#             q_number, q_text = question_match.groups()
#             current_question = f"Q{q_number}"
#             data[current_question] = {"question": q_text, "answers": {}}
#         elif answer_match and current_question:
#             answer_text = answer_match.groups()[0]
#             flow_no = len(data[current_question]["answers"]) + 1
#             flow_no_key = f"FlowNo_{int(q_number)+1}={flow_no}"
#             data[current_question]["answers"][flow_no_key] = answer_text

#     return data

# def rename_columns(df, new_column_names):
#     """
#     Renames dataframe columns based on a list of new column names.
    
#     Parameters:
#     - df (pd.DataFrame): The original DataFrame.
#     - new_column_names (list): A list of new column names corresponding to the DataFrame's columns.
    
#     Returns:
#     - pd.DataFrame: A DataFrame with updated column names.
#     """
#     mapping = {old: new for old, new in zip(df.columns, new_column_names) if new}
#     return df.rename(columns=mapping, inplace=False)

# import re
# import streamlit as st
# import json

# def parse_text_to_json(text_content):
#     """
#     Parses structured text containing survey questions and answers into a JSON-like dictionary.
#     Adjusts FlowNo to start from 2 for the first question as specified.
#     """
#     import re

#     # Initialize variables
#     data = {}
#     current_question = None

#     # Regular expressions for identifying parts of the text
#     question_re = re.compile(r'^(\d+)\.\s+(.*)')
#     answer_re = re.compile(r'^\s+-\s+(.*)')

#     for line in text_content.splitlines():
#         question_match = question_re.match(line)
#         answer_match = answer_re.match(line)

#         if question_match:
#             # New question found
#             q_number, q_text = question_match.groups()
#             current_question = f"Q{q_number}"
#             data[current_question] = {"question": q_text, "answers": {}}
#         elif answer_match and current_question:
#             # Answer found for the current question
#             answer_text = answer_match.groups()[0]
#             # Assuming FlowNo starts at 2 for the first question and increments for each answer within a question
#             flow_no = len(data[current_question]["answers"]) + 1
#             # Adjusting FlowNo to start from 2 for the first question and increment accordingly for each answer
#             flow_no_key = f"FlowNo_{int(q_number)+1}={flow_no}"
#             data[current_question]["answers"][flow_no_key] = answer_text

#     return data

# def custom_sort(col):
#     # Improved regex to capture question and flow numbers accurately
#     match = re.match(r"FlowNo_(\d+)=*(\d*)", col)
#     if match:
#         question_num = int(match.group(1))  # Question number
#         flow_no = int(match.group(2)) if match.group(2) else 0  # Flow number, default to 0 if not present
#         return (question_num, flow_no) 
#     else:
#         return (float('inf'), 0)

# def classify_income(income):
#     if income == 'RM4,850 & below':
#         return 'B40'
#     elif income == 'RM4,851 to RM10,960':
#         return 'M40'
#     elif income in ['RM15,040 & above', 'RM10,961 to RM15,039']:
#         return 'T20'
# import json

# def process_file_content(uploaded_file):
#     """Process the content of the uploaded file."""
#     try:
#         if uploaded_file and uploaded_file.type == "application/json":
#             # Handle JSON file
#             flow_no_mappings = json.loads(uploaded_file.getvalue().decode("utf-8"))
#         else:
#             # Handle plain text file
#             flow_no_mappings = parse_text_to_json(uploaded_file.getvalue().decode("utf-8"))
#         return flow_no_mappings, "Questions and answers parsed successfully.✨", None
#     except Exception as e:
#         return None, None, f"Error processing file: {e}"

# def flatten_json_structure(flow_no_mappings):
#     """Flatten the JSON structure to simplify the mapping access."""
#     if not flow_no_mappings:
#         return {}
#     return {k: v for question in flow_no_mappings.values() for k, v in question["answers"].items()}
