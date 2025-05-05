from fastapi import FastAPI

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
