from fastapi.testclient import TestClient 
from application.quotes import app 

client = TestClient(app) 

def test_get_user_not_found():
    response = client.get("/users/9999")

    assert response.status_code == 404 
    assert response.json()["success"] == False 
    assert response.json()["error"]["message"] == "User not found"

def test_create_user_missing_name():
    response = client.post(
        "/users/103",
        json={
            "email": "test@example.com",
            "phone": "9876543210"
        }
    )

    assert response.status_code == 422
    assert response.json()["success"] == False
    assert response.json()["error"]["message"] == "Validation failed"

def test_create_user_invalid_phone():
    response = client.post(
        "/users/104",
        json={
            "name": "Shifa",
            "email": "test@example.com",
            "phone": "123"
        }
    )

    assert response.status_code == 422
    assert response.json()["success"] == False

def test_create_user_wrong_data_type():
    response = client.post(
        "/users/105",
        json={
            "name": "Shifa",
            "email": "test@example.com",
            "phone": 9876543210
        }
    )

    assert response.status_code == 422

def test_create_user_phone_too_short():
    response = client.post(
        "/users/106",
        json={
            "name": "Shifa",
            "email": "test@example.com",
            "phone": "123456789"
        }
    )

    assert response.status_code == 422
