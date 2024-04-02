from fastapi.testclient import TestClient
from io import BytesIO
from modules.data_cleaner_utils_page1 import process_file
from modules.questionnaire_utils_page2 import parse_questions_and_answers, rename_columns
from modules.keypress_decoder_utils_page3 import parse_text_to_json, custom_sort, classify_income, process_file_content, flatten_json_structure
from streamlit_ivr_survey_automation.fastapiapp.main import app
import json

client = TestClient(app)

# Sample test for `process_file_content` - Adjust as needed for actual implementation
def test_process_file():
    with open("C:\Users\User\Desktop\Invoke Project\Invoke_Streamlit_Survey\streamlit_ivr_survey_automation\fastapiapp\app\csv_files\Broadcast_List_Report_for_PETALING JAYA MANDARIN EVENING.csv", "rb") as file:
        response = client.post(
            "/utilities/",
            data={"action": "process_file"},
            files={"uploaded_file": file}
        )
    assert response.status_code == 200
    # Add specific assertions based on expected response structure

def test_parse_questions_and_answers():
    sample_json_data = '{"question1": {"question": "What is FastAPI?", "answers": {"1": "A web framework"}}}'
    response = client.post(
        "/utilities/",
        data={
            "action": "parse_questions_and_answers",
            "json_data": sample_json_data
        }
    )
    assert response.status_code == 200
    # Assert expected parsed structure

def test_rename_columns():
    sample_df_json = '[{"oldName1": "value1", "oldName2": "value2"}]'
    new_column_names_json = '{"oldName1": "newName1", "oldName2": "newName2"}'
    response = client.post(
        "/utilities/",
        data={
            "action": "rename_columns",
            "json_data": sample_df_json,
            "new_column_names": new_column_names_json
        }
    )
    assert response.status_code == 200
    # Assert new column names in response

def test_parse_text_to_json():
    text_content = "1. Question one\n- Answer 1\n2. Question two\n- Answer 2"
    response = client.post(
        "/utilities/",
        data={
            "action": "parse_text_to_json",
            "text_content": text_content
        }
    )
    assert response.status_code == 200
    # Assert JSON structure of parsed text

def test_custom_sort():
    # Example assuming a specific input and output for custom_sort, adjust as needed
    sort_keys = '["FlowNo_2=1", "FlowNo_3=2"]'
    response = client.post(
        "/utilities/",
        data={
            "action": "custom_sort",
            "sort_keys": sort_keys
        }
    )
    assert response.status_code == 200
    # Assert sorted order

def test_classify_income():
    income = "RM4,850 & below"
    response = client.post(
        "/utilities/",
        data={
            "action": "classify_income",
            "income": income
        }
    )
    assert response.status_code == 200
    assert response.json() == {"income_category": "B40"}

def test_flatten_json_structure():
    sample_json_data = '{"Q1": {"question": "What is FastAPI?", "answers": {"FlowNo_2=1": "A web framework"}}}'
    response = client.post(
        "/utilities/",
        data={
            "action": "flatten_json_structure",
            "json_data": sample_json_data
        }
    )
    assert response.status_code == 200
    # Assert flattened structure

client = TestClient(app)

def test_process_file_content_with_text():
    file_content = BytesIO(b"Sample text content")
    response = client.post(
        "/utilities/",
        data={"action": "process_file_content"},
        files={"uploaded_file": ("C:\Users\User\Desktop\Invoke Project\Invoke_Streamlit_Survey\streamlit_ivr_survey_automation\fastapiapp\app\script_json_files\PJ Scripts with Formatting.txt", file_content, "text/plain")}
    )
    assert response.status_code == 200
    # Add assertions based on expected behavior of process_file_content with text input

def test_process_file_content_with_json():
    # Preparing JSON content for upload
    json_content = json.dumps({"key": "value"})
    response = client.post(
        "/utilities/",
        data={"action": "process_file_content"},
        files={"uploaded_file": ("C:\Users\User\Desktop\Invoke Project\Invoke_Streamlit_Survey\streamlit_ivr_survey_automation\fastapiapp\app\script_json_files\PJ Script JSON Format.json", BytesIO(json_content.encode()), "application/json")}
    )
    assert response.status_code == 200
    # Add assertions based on expected behavior of process_file_content with JSON input
