import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from main import app  # Adjust the import if your file is named differently

client = TestClient(app)

def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World!"}

def test_get_user_sql_injection():
    response = client.get("/users", params={"username": "admin'; DROP TABLE users; --"})
    assert response.status_code == 200
    # Ensure the query is built with the vulnerable input
    assert "DROP TABLE users" in response.json()["query"]

def test_read_file_valid_path(tmp_path):
    # Create a temporary file for testing
    temp_file = tmp_path / "test.txt"
    temp_file.write_text("This is a test file.")
    response = client.get("/read_file", params={"file_path": str(temp_file)})
    assert response.status_code == 200
    assert response.json() == {"content": "This is a test file."}

def test_read_file_invalid_path():
    response = client.get("/read_file", params={"file_path": "/non/existent/file.txt"})
    assert response.status_code == 500
    assert "detail" in response.json()

def test_error_endpoint():
    try:
        response = client.get("/error")
        assert response.status_code == 500  # Should raise a 500 Internal Server Error
    except ZeroDivisionError as err:
        assert "division by zero" in str(err)

def test_upload_file():
    file_content = b"dummy content"
    files = {"file": ("test.txt", file_content, "text/plain")}
    response = client.post("/upload", files=files)
    assert response.status_code == 200
    assert response.json() == {"message": "File uploaded successfully"}

def test_secure_data_with_valid_token():
    response = client.get("/secure-data", params={"token": "1234567890"})
    assert response.status_code == 200
    assert response.json() == {"data": "Sensitive Data"}

def test_secure_data_with_invalid_token():
    response = client.get("/secure-data", params={"token": "wrong_token"})
    assert response.status_code == 403
    assert response.json() == {"message": "Forbidden"}
