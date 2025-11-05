import requests
from jsonschema import validate
from schemas import (
    register_success_schema,
    register_error_schema
)

headers = {
    "x-api-key": "reqres-free-v1",
    "Content-Type": "application/json",
}

# 6. На бизнес-логику: регистрация пользователя

def test_register_success_business_logic():
    register_url = "https://reqres.in/api/register"
    payload = {
        "email": "eve.holt@reqres.in",   # "разрешённый" юзер в reqres
        "password": "pistol",
    }

    response = requests.post(register_url, headers=headers, json=payload)
    assert response.status_code == 200

    body = response.json()

    validate(body, schema=register_success_schema)

    assert body["id"] != 0
    assert isinstance(body["id"], int)
    assert isinstance(body["token"], str)
    assert body["token"] != ""


def test_register_missing_password_business_logic():
    register_url = "https://reqres.in/api/register"
    payload = {
        "email": "sydney@fife"
    }

    response = requests.post(register_url, headers=headers, json=payload)
    assert response.status_code == 400

    body = response.json()

    validate(body, schema=register_error_schema)
    assert body["error"] == "Missing password"
