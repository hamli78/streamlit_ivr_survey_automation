# # #
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from modules.data_cleaner_utils_page1 import process_file
from modules.questionnaire_utils_page2 import parse_questions_and_answers, rename_columns
from modules.keypress_decoder_utils_page3 import parse_text_to_json, custom_sort, classify_income, process_file_content, flatten_json_structure
import pandas as pd
import json

app = FastAPI()

@app.post("/utilities/")
async def utilities_endpoint(
    action: str = Form(...),
    uploaded_file: UploadFile = File(None),
    text_content: str = Form(None),
    json_data: str = Form(None),
    new_column_names: str = Form(None),
    income: str = Form(None),  # For classify_income
    sort_keys: str = Form(None)  # New for custom_sort
):  
    try:
        if action == "process_file":
            if not uploaded_file:
                raise HTTPException(status_code=400, detail="Uploaded file is required for this action.")
            df_complete, phonenum_list, total_calls, total_pickup = process_file(uploaded_file.file)
            return {
                "df_complete": df_complete.to_json(orient="records"),
                "phonenum_list": phonenum_list.to_json(orient="records"),
                "total_calls": total_calls,
                "total_pickup": total_pickup
            }
            
        # Handling file processing
        if action == "process_file_content":
            if not uploaded_file:
                raise HTTPException(status_code=400, detail="Uploaded file is required for this action.")
            processed_data, message, error = await process_file_content(uploaded_file)
            if error:
                raise HTTPException(status_code=500, detail=error)
            return {"processed_data": processed_data, "message": message}
        
        elif action == "parse_questions_and_answers":
            if not json_data:
                raise HTTPException(status_code=400, detail="JSON data is required for this action.")
            parsed_data = parse_questions_and_answers(json.loads(json_data))
            return parsed_data
        elif action == "parse_text_to_json":
            if not text_content:
                raise HTTPException(status_code=400, detail="Text content is required for this action.")
            json_data = parse_text_to_json(text_content)
            return json_data
        elif action == "rename_columns":
            if not json_data or not new_column_names:
                raise HTTPException(status_code=400, detail="JSON data and new column names are required for this action.")
            df = pd.DataFrame(json.loads(json_data))
            updated_df = rename_columns(df, json.loads(new_column_names))
            return updated_df.to_json(orient="records")
        elif action == "flatten_json_structure":
            if not json_data:
                raise HTTPException(status_code=400, detail="JSON data is required for this action.")
            flat_data = flatten_json_structure(json.loads(json_data))
            return flat_data
        
        elif action == "classify_income":
                    if not income:
                        raise HTTPException(status_code=400, detail="Income data is required for this action.")
                    income_category = classify_income(income)
                    return {"income_category": income_category}
                
        # New action for custom_sort
        elif action == "custom_sort":
            if not sort_keys:
                raise HTTPException(status_code=400, detail="Sort keys are required for this action.")
            # Assuming sort_keys is a JSON string representing a list of keys
            keys = json.loads(sort_keys)
            if not isinstance(keys, list):
                raise HTTPException(status_code=400, detail="Sort keys must be a list.")
            sorted_keys = sorted(keys, key=lambda x: custom_sort(x))
            return {"sorted_keys": sorted_keys}

        else:
            raise HTTPException(status_code=400, detail="Unsupported action.")

    
    except Exception as e:
        # General error handling
        raise HTTPException(status_code=500, detail=str(e))
    
    
    
    
# from fastapi import FastAPI, File, UploadFile, HTTPException
# from typing import List
# from modules.data_cleaner_utils_page1 import process_file  # Adjust import based on your actual file processing function
# from streamlit_ivr_survey_automation.fastapiapp.app import schemas  # Ensure this import matches your project structure

# app = FastAPI()

# @app.post("/process-file", response_model=List[schemas.PhoneNumberResponse])
# async def create_upload_file(uploaded_file: UploadFile = File(...)):
#     # Process the uploaded file and extract phone numbers
#     try:
#         processed_data = await process_file(uploaded_file.file)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")
    
#     # Assuming processed_data['phonenum_list'] is a list of phone numbers
#     phone_numbers = processed_data['phonenum_list']

#     # Convert extracted phone numbers to Pydantic models before returning
#     phone_number_responses = [schemas.PhoneNumberResponse(phone_number=phone) for phone in phone_numbers]

#     return phone_number_responses



# from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
# from typing import List
# from sqlalchemy.orm import Session
# from app.modules import schemas
# from app.modules.data_cleaner_utils_page1 import process_file

# app = FastAPI()

# @app.post("/process-file", response_model=List[schemas.PhoneNumberResponse])  # Adjust response model
# async def create_upload_file(uploaded_file: UploadFile = File(...), db: Session = Depends(dependencies.get_db)):
#     # Process the uploaded file and extract phone numbers
#     try:
#         processed_data = await process_file(uploaded_file.file)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")
    
#     # Attempt to create phone numbers in the database
#     created_phone_numbers = []
#     for item in processed_data['phonenum_list']:  # Assuming this is a list of dict or similar
#         phone_number = item['phone_number']  # Adjust based on your actual data structure
#         try:
#             created_phone_number = crud.create_phone_number(db=db, phone_number=phone_number)
#             created_phone_numbers.append(created_phone_number)
#         except Exception as e:
#             db.rollback()
#             raise HTTPException(status_code=400, detail=f"Failed to create phone number: {str(e)}")
    
#     # Commit database changes if all phone numbers are created successfully
#     db.commit()

#     # Convert created phone numbers to Pydantic models (schemas) before returning
#     return [schemas.PhoneNumberResponse.from_orm(phone) for phone in created_phone_numbers]




# from fastapi import FastAPI, UploadFile, Depends, HTTPException
# from typing import List
# from sqlalchemy.orm import Session
# from modules import schemas
# from modules.data_cleaner_utils_page1 import process_file
# from modules import crud
# from modules import dependencies

# app = FastAPI()

# @app.post("/process-file/", response_model=List[schemas.PhoneNumber])
# async def create_upload_file(uploaded_file: UploadFile, db: Session = Depends(dependencies.get_db)):
#     # Your file processing logic here
#     # Assume process_file returns a list of phone numbers in the desired format
#     phonenum_list = await process_file(uploaded_file)
#     try:
#         for item in phonenum_list:
#             # Assuming create_phone_number returns an instance of models.PhoneNumber
#             created_phone_number = crud.create_phone_number(db=db, phone_number=item)
#             # Do something with created_phone_number if needed, e.g., transform it into a response model
#         db.commit()
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=400, detail=str(e))
#     return phonenum_list


# from fastapi import FastAPI, File, UploadFile, Depends
# from sqlalchemy.orm import Session
# from modules import dependencies
# from modules.dependencies import get_db
# from modules.data_cleaner_utils_page1 import process_file  # Adapt the import as necessary
# from fastapi.responses import JSONResponse
# from typing import List

# from modules import crud,  schemas ,dependencies
# from modules import models,dependencies

# app = FastAPI()

# @app.post("/process-file/", response_model=List[schemas.PhoneNumber])
# async def create_upload_file(uploaded_file: UploadFile, db: Session = Depends(get_db)):
#     result = await process_file(uploaded_file)  # This needs to be adapted based on your process_file function
#     phonenum_list = []
#     for item in result["phonenum_list"]:
#         created_phone_number = crud.create_phone_number(db=db, phone_number=schemas.PhoneNumberCreate(phone_number=item['PhoneNo'], user_key_press=""))
#         phonenum_list.append(created_phone_number)
#     db.commit()
#     return phonenum_list





# from fastapi import FastAPI, Depends, HTTPException
# from sqlalchemy.orm import Session
# from modules import crud, models, schemas
# from modules.database import SessionLocal, engine

# models.Base.metadata.create_all(bind=engine)  # Create tables

# app = FastAPI()

# # Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @app.post("/phonenumbers/", response_model=schemas.PhoneNumber)
# def create_phone_number(phone_number: schemas.PhoneNumberCreate, db: Session = Depends(get_db)):
#     db_phone_number = crud.get_phone_number_by_number(db, phone_number=phone_number.phone_number)
#     if db_phone_number:
#         raise HTTPException(status_code=400, detail="Phone number already registered")
#     return crud.create_phone_number(db=db, phone_number=phone_number)




















# from fastapi import FastAPI, File, UploadFile
# from fastapi.responses import JSONResponse
# import pandas as pd
# import numpy as np
# from typing import List
# from starlette.background import BackgroundTasks
# import asyncio
# from concurrent.futures import ThreadPoolExecutor

# app = FastAPI()

# executor = ThreadPoolExecutor(max_workers=4)

# def process_file_sync(uploaded_file):
#     df = pd.read_csv(uploaded_file.file, skiprows=1, names=range(100), engine='python')
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

#     return {
#         "df_complete": df_complete.to_dict(),
#         "phonenum_list": phonenum_list.to_dict(),
#         "total_calls": total_calls,
#         "total_pickup": total_pickup
#     }

# async def process_file(uploaded_file: UploadFile):
#     loop = asyncio.get_event_loop()
#     return await loop.run_in_executor(executor, process_file_sync, uploaded_file)

# @app.post("/process-file/")
# async def create_upload_file(uploaded_file: UploadFile):
#     result = await process_file(uploaded_file)
#     return JSONResponse(content=result)




































































# from fastapi import FastAPI, File, UploadFile, Query
# from fastapi.responses import JSONResponse
# import pandas as pd
# import numpy as np
# import uvicorn
# from modules.data_cleaner_utils_page1 import process_file
# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/", description="This is our first route.")
# async def process_file():
#     return {"message": "hello world"}

# @app.post("/")
# async def post():
#     return {"message": "hello from the post route"}

# @app.put("/{id}")
# async def root():
#     return {"message": "hello from the put route"}

# @app.delete("/",description="This is our last route")
# async def root():
#     return {"message": "hellow from the delete route"}

# @app.get('/users',description="First path parameter useable.")
# async def root():
#     return {"message":"list users route"}

# @app.get("/users/fahmizainal17")
# async def get_current_user():
#     return{"message":"This is the current user"}

# @app.get("/users/{user_id}")
# async def get_user(user_id:str):
#     return{"user_id": user_id}

# #path parameter

# from enum import Enum

# class FoodEnum(str, Enum):
#     fruits = 'fruits'
#     vegetables = "vegetables"
#     dairy = "dairy"
    
# @app.get("/foods/{food_name}")
# async def get_food(food_name:FoodEnum):
#     if food_name ==FoodEnum.vegetables:
#         return {"food_name":food_name,"message":"You are healthy."}
    
#     if food_name.value =="fruits":
#         return{
#             "food_name":food_name,
#             "message":"You are healthy but like sweet things."
#         }
    
#     return {"food_name": food_name, "message":"I like chocolate milk"}

# #query parameter
# fake_items_db = [{"item_name":"Foo"},{"item_name":"Faz"},{"item_name":"Fahmi"}]

# @app.get("/items")
# async def list_items(skip:int=0 , limit:int =10):
#     return fake_items_db[skip:skip+limit]
# #http://localhost:8000/items?limit=1 return first item "item_name":"Foo"
# #http://localhost:8000/items?skip=2 return last item "item_name":"Fahmi"


# @app.get("/items/{item_id}")
# async def get_item(item_id:str, q: str | None=None):
#     if q:
#         return {"item_id":item_id, "q": q}
#     return {"item_id":item_id}

# #type conversion
# fake_items_db = [{"item_name":"Foo"},{"item_name":"Faz"},{"item_name":"Fahmi"}]

# @app.get("/items")
# async def list_items(skip:int=0 , limit:int =10):
#     return fake_items_db[skip:skip+limit]
# #http://localhost:8000/items?limit=1 return first item "item_name":"Foo"
# #http://localhost:8000/items?skip=2 return last item "item_name":"Fahmi"

# #part3 youtube 9:40
# @app.get("/items/{item_id}")
# async def get_item(item_id: str,q: str | None=None, short: bool = Query(False)):
#     item = {"item_id": item_id}
#     if q:
#         item.update({"q":q})
#     if not short:
#         item.update(
#             {
#             "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque mauris"
#             }
#         )
#     return item

# @app.get("/users/{user_id}/items/{item_id}")
# async def get_user_item(user_id: int, item_id: str,sample_query_param: str ,q: str | None=None, short: bool = Query(False)):
#     item = {"item_id":item_id, "owner_id":user_id,"sample_query_param":sample_query_param}
#     if q:
#         item.update({"q":q})
#     if not short:
#         item.update(
#             {
#             "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque mauris"
#             }
#         )
#     return item

# #request body n pydantic
# from pydantic import BaseModel
# from typing import Optional

# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None

# # @app.post("/items")
# # async def create_item(item: Item):
# #     return item

# @app.post("/items")
# async def create_item(item:Item):
#     item_dict = item.dict()
#     if item.tax:
#         price_with_tax = item.price + item.tax
#         item_dict.update({"price_with_tax": price_with_tax})
#     return item_dict

# from fastapi import FastAPI
# from pydantic import BaseModel
# class Item(BaseModel):
    
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
    
# app = FastAPI()

# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     return {"item_id": item_id, **item.dict()}


#############################################################################################################################