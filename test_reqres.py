import requests
from jsonschema import validate
from schemas import (
    post_users,
    put_users,
    list_users_schema,
    single_user_schema,
    register_error_schema
)

BASE_URL = "https://reqres.in/api/users"

headers = {
    "x-api-key": "reqres-free-v1",
    "Content-Type": "application/json",
}

# 1. на каждый из методов GET/POST/PUT/DELETE ручек reqres.in

def test_get_users_list_returns_200_and_matches_schema():
    response = requests.get(BASE_URL, headers=headers, params={"page": 2})
    assert response.status_code == 200

    body = response.json()
    validate(body, schema=list_users_schema)


def test_post_users():
    response = requests.post(
        BASE_URL,
        headers=headers,
        json={"name": "morpheus", "job": "master"},
    )
    body = response.json()
    assert response.status_code == 201
    assert body["name"] == "morpheus"
    assert body["job"] == "master"
    validate(body, schema=post_users)


def test_put_users():
    response = requests.put(
        f"{BASE_URL}/2",
        headers=headers,
        json={"name": "morpheus", "job": "master"},
    )
    body = response.json()
    assert response.status_code == 200
    assert body["name"] == "morpheus"
    assert body["job"] == "master"
    validate(body, schema=put_users)


def test_delete_users():
    response = requests.delete(f"{BASE_URL}/2", headers=headers)
    assert response.status_code == 204


# 2. Позитивные/Негативные тесты на одну из ручек.

def test_get_single_user_positive():
    # Позитивный сценарий: пользователь существует
    response = requests.get(f"{BASE_URL}/2", headers=headers)
    assert response.status_code == 200

    body = response.json()
    assert "data" in body
    assert body["data"]["id"] == 2
    assert "email" in body["data"]
    assert "first_name" in body["data"]
    assert "last_name" in body["data"]

    validate(body, schema=single_user_schema)


def test_get_single_user_negative_not_found():
    # Негативный сценарий: пользователь не существует
    response = requests.get(f"{BASE_URL}/23", headers=headers)
    assert response.status_code == 404

    assert response.json() == {}


# 3. Тесты на разные статус-коды (200 / 201 / 204 / 404 / 400)
# Тесты на статус-коды (200 / 201 / 204) реализованы выше

def test_get_user_404_status():
    not_found_response = requests.get(f"{BASE_URL}/9999", headers=headers)
    assert not_found_response.status_code == 404


def test_register_user_400_status_and_schema():
    register_url = "https://reqres.in/api/register"
    bad_register_response = requests.post(
        register_url,
        headers=headers,
        json={"email": "sydney@fife"},  # без password
    )
    assert bad_register_response.status_code == 400
    body = bad_register_response.json()
    validate(body, schema=register_error_schema)

# С ответом и без ответа
def test_response_with_body():
    # Ручка с ответом: GET одного пользователя
    response = requests.get(f"{BASE_URL}/2", headers=headers)
    assert response.status_code == 200

    # есть тело ответа
    assert response.text != ""

    body = response.json()
    assert isinstance(body, dict)
    assert "data" in body
    assert "id" in body["data"]
    assert "email" in body["data"]


def test_response_without_body():
    # Ручка без тела ответа: DELETE
    response = requests.delete(f"{BASE_URL}/2", headers=headers)
    assert response.status_code == 204

    # реально без тела (пустая строка или пустой байтовый массив)
    assert response.text == "" or response.content == b""

