import json


def test_register_user(test_app_with_db):
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "username": "JohnDosssssse123",
        "email": "john.doe@examssssple.com",
        "password": "StrongPass1!",
        "role": "student",
    }
    response = test_app_with_db.post("/auth/register-user/", json=data)
    assert response.status_code == 201
    assert json.loads(response.content)["message"] == "Registration successful"
