from fastapi import FastAPI, Query, Path, Body
from pydantic import BaseModel, Field

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

@app.get("/friend", description="This is a GET request to get friends")
async def get_friends(friend_id: str | None = Query(
    None,
    min_length=1,
    max_length=100, 
    description="Friend ID is required",
    title="Friend ID",
    alias="friend_id",
    example="12345",
    deprecated=False,
    response_description="This is a response description for friend_id",
    )):
    # This is a GET request to get friend
    # friend_id is an integer with min length 1 and max length 100
    # The Query parameters allow for more control over the input
    # friend_id is a string or None
    return {"message": f"Friend ID: {friend_id}"}

@app.get("/friends", description="This is a GET request to get friends list")
async def get_friends(friend_id: list[int] | None = Query(None, min_length=1, max_length=100, description="Friend ID is required")):
    # This is a GET request to get friends list
    # friend_id is an integer with min length 1 and max length 100
    return {"message": f"Friend ID: {friend_id}"}

@app.get("/friends/hidden", description="This is a GET request to get hidden friends list")
async def get_hidden_friends(friend_id: list[int] | None = Query(None, min_length=1, max_length=100, description="Friend ID is required", include_in_schema=False)):
    # This is a GET request to get hidden friends list
    # friend_id is an integer with min length 1 and max length 100
    # include_in_schema=False means this endpoint will not be included in the OpenAPI schema
    return {"message": f"Friend ID: {friend_id}"}

@app.get("/friends/{friend_id}", description="This is a GET request to get a specific friend")
async def get_friend(*,friend_id: int = Path(..., title="Friend ID", description="This is a friend ID", gt=1, le=1000), q:str):
    # This is a GET request to get a specific friend
    # friend_id is an integer with min value 1 and max value 1000
    # q is a query parameter
    # * means that all parameters after it are keyword-only arguments
    # ... means that this parameter is required
    return {"message": f"Friend ID: {friend_id}, Query: {q}"}


"""
Part 7: Body Multiple Parameters
"""

class ItemWithBody(BaseModel):
    """Item model for creating an item with body parameters
    Attributes:
        name (str): Name of the item
        discription (str | None): Description of the item, optional
        price (float): Price of the item
        tax (float | None): Tax on the item, optional
    """
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class User(BaseModel):
    """User model for creating a user with body parameters
    Attributes:
        username (str): Username of the user
        email (str): Email of the user
    """
    username: str
    email: str

@app.post("/create_item_with_body/{item_id}", description="This is a POST request to create an item with body parameters")
async def create_item_with_body(
    *,
    item_id: int = Path(..., title="Item ID", description="This is an item ID", gt=0, le=1000),
    item_type: str = Query(..., title="Item Type", description="This is an item type", min_length=1, max_length=50),
    item: ItemWithBody = Body(...,embed=True),
    user: User = Body(None),
    importance: int = Body(...),
    ):
    """This is a POST request to create an item with body parameters
    Args:
        item_id (int): ID of the item, must be greater than 0 and less than or equal to 1000
        item_type (str): Type of the item, must be a string with min length 1 and max length 50
        item (ItemWithBody): Item details, must be provided in the body
        user (User | None): User details, optional
        importance (int): Importance level, must be provided in the body    
    Returns:
        dict: A dictionary containing the result of the item creation
    """
    result = {"item_id": item_id, "item_type": item_type}

    if item:
        item_dict = item.model_dump()
        item_dict['total_price'] = item_dict['price'] + (item_dict['tax'] if item_dict['tax'] else item_dict['price'])
        result['item'] = item_dict

    if user:
        user_dict = user.model_dump()
        result['user'] = user_dict

    if importance:
        result['importance'] = importance
    return {"result": result, "message": "Item created successfully with body parameters"}

"""

Part 8: Body - Field

"""

class UserWithField(BaseModel):
    """User model for creating a user with field parameters
    Attributes:
        username (str): Username of the user
        email (str): Email of the user
    """
    username: str = Field(..., title="Username", description="This is a username", min_length=1, max_length=50)
    email: str = Field(..., title="Email", description="This is an email", pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")

@app.post("/create_user_with_field", description="This is a POST request to create a user with field parameters")
async def create_user_with_field(user: UserWithField):
    """This is a POST request to create a user with field parameters
    Args:
        user (UserWithField): User details, must be provided in the body
    Returns:
        dict: A dictionary containing the result of the user creation
    """
    user_dict = user.model_dump()
    return {"user": user_dict, "message": "User created successfully with field parameters"}