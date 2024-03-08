from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import pandas as pd
import numpy as np
import uvicorn
from modules.data_cleaner_utils_page1 import process_file

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def get_process_file(number:int):
    return process_file

@app.get('/burgers')
async def read_burgers():
    burgers = await process_file(2)
    return burgers