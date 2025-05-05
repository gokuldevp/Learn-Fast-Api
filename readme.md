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

## 5. Learning FastAPI Concepts Through Endpoints

### 5.1 Using `async` Functions
FastAPI endpoints are defined as `async` functions to take advantage of Python's asynchronous capabilities. This allows the server to handle multiple requests concurrently, improving performance for I/O-bound operations like database queries or external API calls.

Example:
```python
@app.get("/")
async def get_request():
    return {"message": "This is a GET request"}
```

### 5.2 Adding Descriptions to Endpoints
The `description` parameter in route decorators helps document the purpose of each endpoint. This information is displayed in the interactive API documentation (Swagger UI and ReDoc).

Example:
```python
@app.get("/", description="This is a GET request")
async def get_request():
    return {"message": "This is a GET request"}
```

### 5.3 Using Path Parameters
Path parameters allow dynamic values to be passed in the URL. FastAPI automatically validates and converts these parameters based on their type annotations.

Example:
```python
@app.get("/user/{user_id}")
async def get_user(user_id: int):
    return {"message": f"User ID is {user_id}"}
```
- `user_id` is dynamically extracted from the URL.
- Type annotations (e.g., `int`) ensure that the parameter is validated and converted automatically.

### 5.4 Handling Static and Dynamic Paths
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

### 5.5 Custom Logic in Endpoints
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

### 5.6 HTTP Methods
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

### 5.7 Query Parameters
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
