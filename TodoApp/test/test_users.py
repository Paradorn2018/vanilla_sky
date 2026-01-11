from .utils import *
from ..routers.users import get_current_user, get_db
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = make_override_get_user


def test_return_user(test_user):

    user = test_user

    response = client.get('/user')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == "codingwithroby"
    assert response.json()['email'] == "codingwithrobytest@email.com"
    assert response.json()['first_name'] == "Eric"
    assert response.json()['last_name'] == "Roby"
    assert response.json()['is_active'] == True
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == "(111)-111-111"


def test_change_password_success(test_user):
    response = client.put("/user/password", json={"password": "testpassword", 
                                                  "new_password": "new_password"})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_user):
        response = client.put("/user/password", json={"password": "wrongpassword", 
                                                  "new_password": "new_password"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Error on password change'}


def test_phone_number_success(test_user):
     user = test_user

     response = client.put(f"/user/phone_number/{user.phone_number}")
     assert response.status_code == status.HTTP_204_NO_CONTENT