from fastapi import FastAPI

app = FastAPI()

@app.get("/", description="This is a GET request")
async def get_request():
    return {"message": "This is a GET request"}

@app.post("/", description="This is a POST request")
async def post_request():
    return {"message": "This is a POST request"}

@app.put("/", description="This is a PUT request")
async def put_request():
    return {"message": "This is a PUT request"}