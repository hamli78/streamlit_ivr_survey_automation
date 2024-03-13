from fastapi import FastAPI, File, UploadFile, Query
from fastapi.responses import JSONResponse
import pandas as pd
import numpy as np
import uvicorn
from modules.data_cleaner_utils_page1 import process_file
from fastapi import FastAPI

app = FastAPI()

@app.get("/", description="This is our first route.")
async def process_file():
    return {"message": "hello world"}

@app.post("/")
async def post():
    return {"message": "hello from the post route"}

@app.put("/{id}")
async def root():
    return {"message": "hello from the put route"}

@app.delete("/",description="This is our last route")
async def root():
    return {"message": "hellow from the delete route"}

@app.get('/users',description="First path parameter useable.")
async def root():
    return {"message":"list users route"}

@app.get("/users/fahmizainal17")
async def get_current_user():
    return{"message":"This is the current user"}

@app.get("/users/{user_id}")
async def get_user(user_id:str):
    return{"user_id": user_id}

#path parameter

from enum import Enum

class FoodEnum(str, Enum):
    fruits = 'fruits'
    vegetables = "vegetables"
    dairy = "dairy"
    
@app.get("/foods/{food_name}")
async def get_food(food_name:FoodEnum):
    if food_name ==FoodEnum.vegetables:
        return {"food_name":food_name,"message":"You are healthy."}
    
    if food_name.value =="fruits":
        return{
            "food_name":food_name,
            "message":"You are healthy but like sweet things."
        }
    
    return {"food_name": food_name, "message":"I like chocolate milk"}

#query parameter
fake_items_db = [{"item_name":"Foo"},{"item_name":"Faz"},{"item_name":"Fahmi"}]

@app.get("/items")
async def list_items(skip:int=0 , limit:int =10):
    return fake_items_db[skip:skip+limit]
#http://localhost:8000/items?limit=1 return first item "item_name":"Foo"
#http://localhost:8000/items?skip=2 return last item "item_name":"Fahmi"


@app.get("/items/{item_id}")
async def get_item(item_id:str, q: str | None=None):
    if q:
        return {"item_id":item_id, "q": q}
    return {"item_id":item_id}

#type conversion
fake_items_db = [{"item_name":"Foo"},{"item_name":"Faz"},{"item_name":"Fahmi"}]

@app.get("/items")
async def list_items(skip:int=0 , limit:int =10):
    return fake_items_db[skip:skip+limit]
#http://localhost:8000/items?limit=1 return first item "item_name":"Foo"
#http://localhost:8000/items?skip=2 return last item "item_name":"Fahmi"

#part3 youtube 9:40
@app.get("/items/{item_id}")
async def get_item(item_id: str,q: str | None=None, short: bool = Query(False)):
    item = {"item_id": item_id}
    if q:
        item.update({"q":q})
    if not short:
        item.update(
            {
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque mauris"
            }
        )
    return item

@app.get("/users/{user_id}/items/{item_id}")
async def get_user_item(user_id: int, item_id: str,sample_query_param: str ,q: str | None=None, short: bool = Query(False)):
    item = {"item_id":item_id, "owner_id":user_id,"sample_query_param":sample_query_param}
    if q:
        item.update({"q":q})
    if not short:
        item.update(
            {
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque mauris"
            }
        )
    return item

#request body n pydantic
from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

# @app.post("/items")
# async def create_item(item: Item):
#     return item

@app.post("/items")
async def create_item(item:Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

