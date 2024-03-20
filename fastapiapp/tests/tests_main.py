from fastapi.testclient import TestClient
from app.main import app  # Adjust the import path according to your project structure

client = TestClient(app)

def process_file():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def process_file():
    files = {
        'uploaded_file': ('filename.csv', open('path_to_your_file.csv', 'rb'), 'text/csv')
    }
    response = client.post("/process-file", files=files)
    assert response.status_code == 200
    # Add more assertions here based on the expected response structure
#
#
