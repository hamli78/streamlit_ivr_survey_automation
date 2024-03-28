import re
import json

def parse_text_to_json(text_content):
            """
            Parses structured text containing survey questions and answers into a JSON-like dictionary, with an adjustment such that
            the FlowNo starts from 2 for the first question.

            Parameters:
            - text_content (str): The text content containing structured survey questions and answers.

            Returns:
            - dict: A dictionary representation of the parsed text content where each question is a key and its value
            is another dictionary containing the question text and a dictionary of answers.
            Answers are keyed by their FlowNo adjusted to start from 2 for the first question.
            """

            # Initialize variables
            data = {}
            current_question = None

            # Regular expressions for identifying parts of the text
            question_re = re.compile(r'^(\d+)\.\s+(.*)')
            answer_re = re.compile(r'^\s+-\s+(.*)')

            for line in text_content.splitlines():
                question_match = question_re.match(line)
                answer_match = answer_re.match(line)

                if question_match:
                    # New question found
                    q_number, q_text = question_match.groups()
                    current_question = f"Q{q_number}"
                    data[current_question] = {"question": q_text, "answers": {}}
                elif answer_match and current_question:
                    # Answer found for the current question
                    answer_text = answer_match.groups()[0]
                    # Assuming FlowNo starts at 2 for the first question and increments for each answer within a question
                    flow_no = len(data[current_question]["answers"]) + 1
                    # Adjusting FlowNo to start from 2 for the first question and increment accordingly for each answer
                    flow_no_key = f"FlowNo_{int(q_number)+1}={flow_no}"
                    data[current_question]["answers"][flow_no_key] = answer_text

            return data

def custom_sort(col):
            """
            A custom sorting function designed to accurately capture and sort items based on question and flow numbers extracted from a given string.

            Parameters:
            - col (str): The string containing the item to be sorted, expected to be in the format "FlowNo_[QuestionNumber]=[FlowNumber]".

            Returns:
            - tuple: A tuple where the first element is the question number (as an integer) and the second element is the flow number (also as an integer).
                    If the flow number is not present in the string, it defaults to 0. Non-matching strings are placed at the end.
            """
            # Improved regex to capture question and flow numbers accurately
            match = re.match(r"FlowNo_(\d+)=*(\d*)", col)
            if match:
                question_num = int(match.group(1))  # Question number
                flow_no = int(match.group(2)) if match.group(2) else 0  # Flow number, default to 0 if not present
                return (question_num, flow_no) 
            else:
                return (float('inf'), 0)

def classify_income(income):
            """
            Classifies an income level into one of three categories: B40, M40, or T20, based on income ranges specific to Malaysian economic demarcations.

            Parameters:
            - income (str): The income level as a string.

            Returns:
            - str: A string representing the income classification ('B40', 'M40', or 'T20').
                Returns None if the income does not match any category.
            """
            if income == 'RM4,850 & below':
                return 'B40'
            elif income == 'RM4,851 to RM10,960':
                return 'M40'
            elif income in ['RM15,040 & above', 'RM10,961 to RM15,039']:
                return 'T20'


def process_file_content(uploaded_file):
            """
            Processes the content of an uploaded file, distinguishing between JSON and plain text formats, and parses it accordingly.

            Parameters:
            - uploaded_file (file): The file uploaded by the user, expected to be either a plain text file or a JSON file.

            Returns:
            - tuple: A tuple containing the parsed content (as a dictionary), a success message, or an error message.
                    The tuple structure is (dict, str, None) for successful parsing, and (None, None, str) for errors.
            """
            try:
                if uploaded_file and uploaded_file.type == "application/json":
                    # Handle JSON file
                    flow_no_mappings = json.loads(uploaded_file.getvalue().decode("utf-8"))
                else:
                    # Handle plain text file
                    flow_no_mappings = parse_text_to_json(uploaded_file.getvalue().decode("utf-8"))
                return flow_no_mappings, "Questions and answers parsed successfully.✨", None
            except Exception as e:
                return None, None, f"Error processing file: {e}"

def flatten_json_structure(flow_no_mappings):
            """
            Flattens the JSON structure obtained from parsing survey questions and answers to simplify access to mappings.

            Parameters:
            - flow_no_mappings (dict): A dictionary representation of survey questions and answers.

            Returns:
            - dict: A flattened dictionary where each key is a "FlowNo" mapping and its value is the corresponding answer text.
            """
            if not flow_no_mappings:
                return {}
            return {k: v for question in flow_no_mappings.values() for k, v in question["answers"].items()}
