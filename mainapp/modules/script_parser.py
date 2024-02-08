import re

# Function to parse questions from the uploaded .txt file
def parse_questions_and_answers(file_contents):
    """
    Parses the uploaded .txt file to extract questions and their corresponding answers.
    Expected file format:
        1. Question text
        - Answer 1
        - Answer 2
        ...
    Returns a dictionary where keys are 'Q{question_number}' and values are dictionaries
    containing the question text and a list of its answers.
    """
    questions_and_answers = {}
    current_question_key = None

    for line in file_contents.split('\n'):
        line = line.strip()
        if line.startswith('-'):  # This line is an answer
            answer_text = line[1:].strip()  # Remove the dash and leading whitespace
            if current_question_key and answer_text:  # Make sure there's a question to attach this answer to
                questions_and_answers[current_question_key]['answers'].append(answer_text)
        else:
            match = re.match(r"(\d+)\.\s*(.*)", line)
            if match:
                question_number, question_text = match.groups()
                current_question_key = f"Q{int(question_number)}"
                # Initialize the dictionary entry for this question with the question text and an empty list for answers
                questions_and_answers[current_question_key] = {'question': question_text.strip(), 'answers': []}

    return questions_and_answers

if __name__ == "__main__":
    parse_questions_and_answers()