# FastAPI Learning Project

This repository documents my journey of learning FastAPI. Below are the steps I have completed so far:

## 1. WSL Setup
- Installed **Windows Subsystem for Linux (WSL)**.
- Set up a Linux distribution (e.g., Ubuntu) for development.
- Verified the installation using `wsl --list --verbose`.

## 2. Installation
- Installed Python and pip in the WSL environment.
- Set up a virtual environment using:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
- Installed FastAPI and Uvicorn:
    ```bash
    pip install fastapi uvicorn
    ```

## 3. New User Guide
- **Activate the virtual environment**:
    ```bash
    source venv/bin/activate
    ```
- **Run the FastAPI application**:
    ```bash
    uvicorn main:app --reload
    ```
    Replace `main` with the name of your Python file containing the FastAPI app.

- **Access the application**:
    Open your browser and navigate to `http://127.0.0.1:8000`.

- **Interactive API Docs**:
    - Swagger UI: `http://127.0.0.1:8000/docs`
    - ReDoc: `http://127.0.0.1:8000/redoc`

## 4. Running Files
- Ensure the virtual environment is active.
- Use `uvicorn` to run your FastAPI application as shown above.

### Additional Ways to Run FastAPI
- **Run with auto-reload** (useful during development):
    ```bash
    uvicorn main:app --reload
    ```

- **Change the default port** (e.g., run on port 8080):
    ```bash
    uvicorn main:app --reload --port 8080
    ```

- **Bind to a specific host** (e.g., make the app accessible on your network):
    ```bash
    uvicorn main:app --reload --host 0.0.0.0
    ```

- **Run in production mode** (without auto-reload):
    ```bash
    uvicorn main:app
    ```

- **Specify the number of workers** (for handling more requests):
    ```bash
    uvicorn main:app --workers 4
    ```

# Part 1: Introductions
## 1. Learning FastAPI Concepts Through Endpoints

### 1.1 Using `async` Functions
FastAPI endpoints are defined as `async` functions to take advantage of Python's asynchronous capabilities. This allows the server to handle multiple requests concurrently, improving performance for I/O-bound operations like database queries or external API calls.

Example:
```python
@app.get("/")
async def get_request():
    return {"message": "This is a GET request"}
```

### 1.2 Adding Descriptions to Endpoints
The `description` parameter in route decorators helps document the purpose of each endpoint. This information is displayed in the interactive API documentation (Swagger UI and ReDoc).

Example:
```python
@app.get("/", description="This is a GET request")
async def get_request():
    return {"message": "This is a GET request"}
```

# Part 2: Using Path Parameters
### 2.1 Using Path Parameters
Path parameters allow dynamic values to be passed in the URL. FastAPI automatically validates and converts these parameters based on their type annotations.

Example:
```python
@app.get("/user/{user_id}")
async def get_user(user_id: int):
    return {"message": f"User ID is {user_id}"}
```
- `user_id` is dynamically extracted from the URL.
- Type annotations (e.g., `int`) ensure that the parameter is validated and converted automatically.

### 2.2 Handling Static and Dynamic Paths
When defining routes, static paths (e.g., `/user/me`) should be declared before dynamic paths (e.g., `/user/{user_id}`) to avoid conflicts.

Example:
```python
@app.get("/user/me")
async def get_current_user():
    return {"message": "This is a GET request for the current user"}

@app.get("/user/{user_id}")
async def get_user(user_id: int):
    return {"message": f"User ID is {user_id}"}
```

### 2.3 Custom Logic in Endpoints
Endpoints can include custom logic, such as checking conditions or performing calculations. For example, the `/user/adult/{age}` endpoint determines if a user is an adult based on their age.

Example:
```python
class User:
    def __init__(self, age: int):
        self.age = age

    def is_adult(self):
        if self.age < 0:
            return "Invalid age"
        elif self.age >= 18:
            return "User is adult"
        return "User is not adult"

@app.get("/user/adult/{age}")
async def get_is_user_adult(age: int):
    user = User(age)
    return {"message": user.is_adult()}
```
- This demonstrates how to encapsulate logic in a class and use it within an endpoint.

### 2.4 HTTP Methods
FastAPI supports multiple HTTP methods (e.g., GET, POST, PUT). Each method is used for a specific purpose:
- **GET**: Retrieve data.
- **POST**: Create new data.
- **PUT**: Update existing data.

Example:
```python
@app.post("/")
async def post_request():
    return {"message": "This is a POST request"}
```

---
# Part 3: Using Query Parameters
### 3.1 Query Parameters
Query parameters are used to pass additional data to endpoints via the URL. In FastAPI, query parameters are defined as function arguments that are not part of the path parameters.

#### How to Use Query Parameters
- **Required Query Parameters**: These must be included in the URL.
    Example: `/user/item?user_id=123`
- **Optional Query Parameters**: These can be omitted from the URL. If omitted, they take the default value specified in the function signature.
    Example: `/user/item?user_id=123&item_id=456` or `/user/item?user_id=123`

#### Example
```python
@app.get("/user/item", description="This is a GET request for user item using query params")
async def get_user_item(user_id: int, item_id: int = None):
    # user_id is a required query parameter
    # item_id is an optional query parameter
    if item_id:
        return {"message": f"User ID: {user_id}, Item ID: {item_id}"}
    return {"message": f"User ID: {user_id}"}
```

#### Key Points:
1. **Required Query Parameter**:
    ```python
    async def get_user_item(user_id: int):
        return {"message": f"User ID: {user_id}"}
    ```
    URL: `/user/item?user_id=123`

2. **Optional Query Parameter**:
    ```python
    async def get_user_item(user_id: int, item_id: int = None):
        if item_id:
            return {"message": f"User ID: {user_id}, Item ID: {item_id}"}
        return {"message": f"User ID: {user_id}"}
    ```
    URL: `/user/item?user_id=123&item_id=456` or `/user/item?user_id=123`

3. **Default Value for Query Parameter**:
    ```python
    async def get_user_item(user_id: int, item_id: int = 0):
        return {"message": f"User ID: {user_id}, Item ID: {item_id}"}
    ```
    URL: `/user/item?user_id=123` (item_id defaults to `0`)

---
# Part 4:  Request Body
### 4.1 Working with Request Bodies Using Pydantic Models

FastAPI uses Pydantic models to define and validate the structure of request bodies for endpoints, especially for POST and PUT requests. This helps ensure that the data received is well-structured and type-safe.

#### Defining a Pydantic Model

```python
from pydantic import BaseModel

class Item(BaseModel):
    """
    Item model for creating an item

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
```

#### Creating an Item

- Use the model as a parameter in your endpoint to automatically parse and validate the incoming JSON.
- You can add logic to process or enrich the data before returning a response.

```python
@app.post("/create_item", description="This is a POST request to create an item")
async def create_item(item: Item):
    # item is a Pydantic model
    item_dict = item.model_dump()
    item_dict['total_price'] = item_dict['price'] + (item_dict['tax'] if item_dict['tax'] else item_dict['price'])
    return {"item": item_dict, "message": "Item created successfully"}
```

#### Updating an Item

- You can combine path parameters, request bodies, and query parameters in a single endpoint.

```python
@app.put("/update_item/{item_id}", description="This is a PUT request to update an item")
async def update_item(item_id: int, item: Item, item_type: str = "Cloths"):
    # item_id is an integer (from path)
    # item is a Pydantic model (from request body)
    # item_type is a string with default value "Cloths" (from query)
    item_dict = item.model_dump()
    item_dict['type'] = item_type
    item_dict['item_id'] = item_id
    item_dict['total_price'] = item_dict['price'] + (item_dict['tax'] if item_dict['tax'] else item_dict['price'])
    return {"item": item_dict, "message": "Item updated successfully"}
```

**Key Points:**
- Use Pydantic models to define the expected structure for request bodies.
- FastAPI automatically validates and parses the incoming data.
- You can combine path, query, and body parameters in your endpoints.
- Optional fields can be specified with `| None` and default values.

---

# Part 5:  Query Parameters and String Validation

FastAPI provides powerful tools for validating and customizing query parameters using the `Query` class. This allows you to enforce constraints such as minimum/maximum length, provide descriptions, set aliases, mark parameters as deprecated, and more.

### 5.1 String Query Parameter Validation

You can use `Query` to add validation and metadata to query parameters. For example, you can specify minimum and maximum length, add a description, set a title, provide an alias, and even mark a parameter as deprecated.

```python
from fastapi import Query

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
    # friend_id is a string or None, with length constraints and metadata
    return {"message": f"Friend ID: {friend_id}"}
```

**Key Points:**
- `min_length` and `max_length` enforce string length.
- `description`, `title`, and `example` improve API documentation.
- `alias` allows you to use a different name in the query string.
- `deprecated` marks the parameter as deprecated in the docs.
- `response_description` adds a description to the response in the docs.

---

### 5.2 List Query Parameters and Validation

You can also accept lists as query parameters and apply validation to each item in the list.

```python
@app.get("/friends", description="This is a GET request to get friends list")
async def get_friends(friend_id: list[int] | None = Query(
    None, min_length=1, max_length=100, description="Friend ID is required"
)):
    # friend_id is a list of integers, with length constraints
    return {"message": f"Friend ID: {friend_id}"}
```

- Pass multiple values in the query string: `/friends?friend_id=1&friend_id=2&friend_id=3`
- `min_length` and `max_length` apply to each string value in the list.

---

### 5.3 Hiding Endpoints from OpenAPI Schema

You can hide endpoints from the automatically generated OpenAPI schema by setting `include_in_schema=False` in the `Query` parameters.

```python
@app.get("/friends/hidden", description="This is a GET request to get hidden friends list")
async def get_hidden_friends(friend_id: list[int] | None = Query(
    None, min_length=1, max_length=100, description="Friend ID is required", include_in_schema=False
)):
    # This endpoint will not appear in the OpenAPI docs
    return {"message": f"Friend ID: {friend_id}"}
```

---

**Summary:**
- Use `Query` for advanced query parameter validation and documentation.
- You can control string length, provide metadata, accept lists, and hide endpoints from docs.
- These features help you build robust, well-documented, and user-friendly APIs.

---

# Part 6: Path Parameters and Numeric Validation

FastAPI allows you to validate and document path parameters using the `Path` class. This enables you to enforce constraints such as minimum and maximum values, provide descriptions, and more.

### 6.1 Numeric Path Parameter Validation

You can use `Path` to add validation and metadata to path parameters. For example, you can specify minimum (`gt`, `ge`) and maximum (`lt`, `le`) values, add a description, and set a title.

```python
from fastapi import Path

@app.get("/friends/{friend_id}", description="This is a GET request to get a specific friend")
async def get_friend(
    *,
    friend_id: int = Path(
        ...,  # Required parameter
        title="Friend ID",
        description="This is a friend ID",
        gt=1,  # Greater than 1
        le=1000  # Less than or equal to 1000
    ),
    q: str
):
    # friend_id is an integer with min value 1 and max value 1000
    # q is a query parameter
    # * means that all parameters after it are keyword-only arguments
    # ... means that this parameter is required
    return {"message": f"Friend ID: {friend_id}, Query: {q}"}
```

**Key Points:**
- Use `Path` to add validation and documentation to path parameters.
- `gt`, `ge`, `lt`, `le` allow you to set numeric constraints.
- `title` and `description` improve the generated API docs.
- `...` (Ellipsis) makes the parameter required.
- Placing `*` in the function signature makes all following parameters keyword-only, improving clarity and flexibility.

---

# Part 7: Body Multiple Parameters

FastAPI allows you to receive multiple body parameters in a single request by using Pydantic models and the `Body` class. This is useful when you want to accept complex, structured data for different entities in the same endpoint, along with additional primitive values.

### 7.1 Defining Multiple Body Models

You can define multiple Pydantic models to represent different parts of the request body. For example:

```python
from pydantic import BaseModel

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
```

### 7.2 Endpoint with Multiple Body Parameters

You can combine path, query, and multiple body parameters in a single endpoint. Use `Body(...)` to explicitly declare body parameters, and `embed=True` to nest the model under its name in the request body.

```python
from fastapi import Path, Query, Body

@app.post("/create_item_with_body/{item_id}", description="This is a POST request to create an item with body parameters")
async def create_item_with_body(
    *,
    item_id: int = Path(..., title="Item ID", description="This is an item ID", gt=0, le=1000),
    item_type: str = Query(..., title="Item Type", description="This is an item type", min_length=1, max_length=50),
    item: ItemWithBody = Body(..., embed=True),
    user: User = Body(None),
    importance: int = Body(...),
):
    """
    This is a POST request to create an item with body parameters

    Args:
        item_id (int): ID of the item, must be greater than 0 and less than or equal to 1000 (path parameter)
        item_type (str): Type of the item, must be a string with min length 1 and max length 50 (query parameter)
        item (ItemWithBody): Item details, must be provided in the body (embedded)
        user (User | None): User details, optional (body)
        importance (int): Importance level, must be provided in the body (body)
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
```

---

### 7.3 Explanation of Each Parameter

- **item_id**:  
  - Type: `int` (Path parameter)
  - Constraints: Must be greater than 0 and less than or equal to 1000.
  - Usage: Uniquely identifies the item being created.

- **item_type**:  
  - Type: `str` (Query parameter)
  - Constraints: String with minimum length 1 and maximum length 50.
  - Usage: Specifies the type/category of the item.

- **item**:  
  - Type: `ItemWithBody` (Body parameter, embedded)
  - Usage: Contains the main details of the item (name, description, price, tax).
  - Note: `embed=True` means the JSON body should have an `"item"` key.

- **user**:  
  - Type: `User` (Body parameter, optional)
  - Usage: Optionally includes user information related to the item.

- **importance**:  
  - Type: `int` (Body parameter)
  - Usage: Represents the importance level of the item.  
  - **Importance**:  
    - This parameter can be used to prioritize items, flag urgent items, or drive business logic based on its value.
    - It is required and must be included in the request body.

---

**Summary:**
- You can combine path, query, and multiple body parameters in a single FastAPI endpoint.
- Use Pydantic models for structured data and `Body(...)` for explicit body parameters.
- `importance` is a required integer in the body, useful for prioritization or business rules.
- This approach allows for flexible and well-documented API endpoints that accept complex input.

---

# Part 8: Body - Field

FastAPI and Pydantic allow you to add extra validation and metadata to individual fields in your models using the `Field` class. This is useful for enforcing constraints (like length or regex patterns) and improving the generated API documentation.

### 8.1 Defining a Model with Field Parameters

You can use `Field(...)` to specify requirements such as minimum/maximum length, regex patterns, titles, and descriptions for each field.

```python
from pydantic import BaseModel, Field

class UserWithField(BaseModel):
    """User model for creating a user with field parameters
    Attributes:
        username (str): Username of the user
        email (str): Email of the user
    """
    username: str = Field(
        ..., 
        title="Username", 
        description="This is a username", 
        min_length=1, 
        max_length=50
    )
    email: str = Field(
        ..., 
        title="Email", 
        description="This is an email", 
        pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$"
    )
```

- `...` means the field is required.
- `title` and `description` improve the OpenAPI docs.
- `min_length` and `max_length` enforce string length.
- `pattern` enforces a regex pattern (here, for a valid email).

### 8.2 Endpoint Using the Model with Field Parameters

```python
@app.post("/create_user_with_field", description="This is a POST request to create a user with field parameters")
async def create_user_with_field(user: UserWithField):
    """
    This is a POST request to create a user with field parameters

    Args:
        user (UserWithField): User details, must be provided in the body
    Returns:
        dict: A dictionary containing the result of the user creation
    """
    user_dict = user.model_dump()
    return {"user": user_dict, "message": "User created successfully with field parameters"}
```

---

### 8.3 Explanation

- **username**:  
  - Type: `str`
  - Required: Yes
  - Constraints: Minimum length 1, maximum length 50
  - Metadata: Title and description for docs

- **email**:  
  - Type: `str`
  - Required: Yes
  - Constraints: Must match the provided regex pattern for emails
  - Metadata: Title and description for docs

**Summary:**
- Use `Field(...)` in Pydantic models to add validation and documentation to individual fields.
- This ensures your API receives well-structured and validated data, and the docs are clear for users.