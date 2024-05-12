from fastapi import FastAPI, Form, Query
from enum import Enum
from pydantic import BaseModel
from typing import Annotated


app = FastAPI()

# First FastAPI endpoint
@app.get("/")
async def root():
    return {"message": "Hello World"}

# Path parameters
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

# Limiting the values of path parameters using Enum, here the set of values are wroted in a Enum class and in the view pass the class as a variable type
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

# Passing file path as path parameters
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

# Query params, Here the wow is an optional parameter, to declare optional parameter, we need to provide default value
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10, wow: int = None):
    print(wow)
    return fake_items_db[skip : skip + limit]

# query parameter that is mandatory becuase it doen't have defaults value
@app.get("/items1/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item


# To get json data from request we need to import BaseModel and create a class with some random name and include the fields to be received from the request, then pass the class as a datatype(the type we need to specify in parameter for a function) to the view function
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/details/")
async def create_item(item: Item):
    return item

# Here the item JSON data is modefied and gives modified JSON object
@app.post("/items/details/modify/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        tax_amount = item.price * item.tax / 100
        price_with_tax = item.price + tax_amount
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

# Request body + path parameters
@app.put("/items/details/modify/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}

# Request body + path + query parameters¶
@app.put("/items/details/modify/q_params/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result

# Query parameter with additional validation, for that we need to import Query from fastapi, Here max_lenght allowed is 50
@app.get("/items/modify_q_params_validations/")
async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# List of Query parameters, we can give values like "?q=10&q=20&q=30"
@app.get("/items/list_of_params/mandatory/")
async def read_items(q: Annotated[list[str], Query()]):
    query_items = {"q": q}
    return query_items

# Default value for list of query parameteres
@app.get("/items/list_of_params/optional/")
async def read_items(q: Annotated[list[str], Query()] = ["foo", "bar"]):
    query_items = {"q": q}
    return query_items

# To get form data from request we need to import "Form" from fastapi
@app.post("/submit/")
async def submit_form(username: str = Form(...), password: str = Form(...)):
    return {"username": username, "password": password}

# passing default value to form data fields
@app.post("/submit_default/")
async def submit_form(username: str = Form(default="default_username"), password: str = Form(default="default_password")):
    return {"username": username, "password": password}

