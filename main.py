import os

from fastapi import FastAPI, Depends, HTTPException, Query, Request
from fastapi.responses import JSONResponse

app = FastAPI()

# Example of hardcoded secrets
API_SECRET = "1234567890"

@app.get("/")
def index():
    return {"message": "Hello World!"}

# Example of improper handling of user input (SQL Injection Vulnerability)
@app.get("/users")
def get_user(username: str):
    query = f"SELECT * FROM users WHERE username = '{username}';"  # Vulnerable to SQL injection
    return {"query": query}

# Example of directory traversal vulnerability
@app.get("/read_file")
def read_file(file_path: str):
    try:
        with open(file_path, "r") as file:
            return {"content": file.read()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Example of improper exception handling
@app.get("/error")
def error_endpoint():
    return 1 / 0  # Will cause an unhandled ZeroDivisionError

# Example of insecure configuration
@app.post("/upload")
async def upload_file(file: Request):
    # Directly saving the file without validation
    with open("uploaded_file", "wb") as f:
        f.write(await file.body())
    return {"message": "File uploaded successfully"}

# Example of improper authentication (no validation)
@app.get("/secure-data")
def secure_data(token: str = Query(...)):
    if token == API_SECRET:
        return {"data": "Sensitive Data"}
    else:
        return JSONResponse(status_code=403, content={"message": "Forbidden"})