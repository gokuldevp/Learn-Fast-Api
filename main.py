from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/", description="This is a GET request")
async def get_request():
    # This is a GET request
    return {"message": "This is a GET request"}

@app.post("/", description="This is a POST request")
async def post_request():
    # This is a POST request
    return {"message": "This is a POST request"}

@app.put("/", description="This is a PUT request")
async def put_request():
    # This is a PUT request
    return {"message": "This is a PUT request"}

@app.get("/user", description="This is a GET request for user")
async def get_user():
    # This is a GET request for user
    return {"message": "This is a GET request for user"}

@app.get("/user/me", description="This is a GET request for current user") 
async def get_current_user():
    # if a static and dynamic path are used together, the static path should be defined first
    return {"message": "This is a GET request for current user"}

@app.get("/user/item", description="This is a GET request for user item using query params")
async def get_user_item(user_id: int, item_id: int=None):
    # This is a GET request for user item using query params
    # user_id is an integer
    # item_id is an optional integer
    if item_id:
        return {"message": f"User ID: {user_id}, Item ID: {item_id}"}
    return {"message": f"User ID: {user_id}"}

@app.get("/user/{user_id}", description="This is a GET request for a specific item")
async def get_item(user_id):
    # This is a GET request for a specific item
    # user_id is a string by default
    # if a static and dynamic path are used together, the static path should be defined first
    return {"message": user_id}

@app.post("/user/{user_id}", description="This is a GET request for a specific item")
async def get_item_int(user_id: int): 
    # This is a GET request for a specific item
    # user_id is an integer
    # if a static and dynamic path are used together, the static path should be defined first
    return {"message": user_id}

class User:
    def __init__(self, age: int):
        self.age = age
    
    def is_adult(self):
        if self.age < 0:
            return "Invalid age"
        elif self.age >= 18:
            return "User is adult"
        return "User is not adult"
    
@app.get("/user/adult/{age}", description="This is a GET request to check if user is adult")
async def get_is_user_adult(age: int):
    # This is a GET request for check user is adult or not
    # age is an integer
    user = User(age)
    return {"message": user.is_adult()}

class Item(BaseModel):
    """Item model for creating an item
    Attributes:
        name (str): Name of the item
        discription (str | None): Description of the item, optional
        price (float): Price of the item
        tax (float | None): Tax on the item, optional
    """
    name: str
    discription: str | None = None
    price: float
    tax: float | None = None

@app.post("/create_item", description="This is a POST request to create an item")
async def create_item(item: Item):
    # This is a POST request to create an item
    # item is a Pydantic model
    item_dict = item.model_dump()
    item_dict['total_price'] = item_dict['price'] + (item_dict['tax'] if item_dict['tax'] else item_dict['price'])
    return {"item": item_dict, "message": "Item created successfully"}

@app.put("/update_item/{item_id}", description="This is a PUT request to update an item")
async def update_item(item_id:int, item: Item, item_type: str = "Cloths"):
    # This is a PUT request to update an item
    # item_id is an integer
    # item is a Pydantic model
    # type is a string with default value "Cloths"
    item_dict = item.model_dump()
    item_dict['type'] = item_type
    item_dict['item_id'] = item_id
    item_dict['total_price'] = item_dict['price'] + (item_dict['tax'] if item_dict['tax'] else item_dict['price'])
    return {"item": item_dict, "message": "Item updated successfully"}