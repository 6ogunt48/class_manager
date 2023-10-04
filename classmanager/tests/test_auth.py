import json


def test_register_user(test_app_with_db):
    data = {
        "first_name": "kola",
        "last_name": "bouncer",
        "username": "kolaBouncer23",
        "email": "kola@kola.com",
        "password": "StrongPass1!",
        "role": "student",
    }
    response = test_app_with_db.post("/auth/register-user/", json=data)
    assert response.status_code == 201
    assert json.loads(response.content)["message"] == "Registration successful"


def test_login_valid_user(test_app_with_db):
    # First register a user
    data = {
        "first_name": "Jane",
        "last_name": "Doe",
        "username": "Apprentice12",
        "email": "jane.doe@example.com",
        "password": "StrongPass1!",
        "role": "student",
    }
    test_app_with_db.post("/auth/register-user/", json=data)

    # Now login
    login_data = {
        "username": "Apprentice12",
        "password": "StrongPass1!"
    }
    response = test_app_with_db.post("/auth/login/", json=login_data)
    assert response.status_code == 200


def test_change_password(test_app_with_db):
    # Create a user
    data = {
        "first_name": "Janet",
        "last_name": "max",
        "username": "Mark12DoeWest",
        "email": "mark@mark.com",
        "password": "StrongPass1!",
        "role": "student",
    }
    test_app_with_db.post("/auth/register-user/", json=data)

    # Change password
    change_password_data = {
        "username": "Mark12DoeWest",
        "password": "StrongPass1!",
        "new_password": "NewStrongPass1!"
    }
    response = test_app_with_db.post("/auth/change-password/", json=change_password_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Password changed successfully"
