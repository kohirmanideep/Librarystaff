from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def get_staff_members():
    response = client.get('/staff/')
    assert response.status_code ==200
    
def get_staff():
    response = client.get('/get/staff/1')
    assert response.status_code == 200