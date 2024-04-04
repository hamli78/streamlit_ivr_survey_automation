# # #
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from app.modules.data_cleaner_utils_page1 import process_file
from app.modules.questionnaire_utils_page2 import parse_questions_and_answers, rename_columns
from app.modules.keypress_decoder_utils_page3 import parse_text_to_json, custom_sort, classify_income, process_file_content, flatten_json_structure
import pandas as pd
import json

app = FastAPI()
