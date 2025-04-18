from config import settings
from fastapi import status
from starlette.testclient import TestClient


def test_read_users(client: TestClient):
    response = client.get(
        url="/users/",
        headers={"Authorization": settings.API_KEY.get_secret_value()},
    )
    assert response.status_code == status.HTTP_200_OK
    users = response.json()
    assert len(users) == 2
    assert users[0]["name"] == "Rick"
    assert users[1]["name"] == "Morty"


def test_read_user_me(client: TestClient):
    response = client.get(
        url="/users/me",
        headers={"Authorization": settings.API_KEY.get_secret_value()},
    )
    assert response.status_code == status.HTTP_200_OK
    user = response.json()
    assert user["name"] == "Fra"


def test_read_user(client: TestClient):
    name = "TestUser"
    response = client.get(
        url=f"/users/{name}",
        headers={"Authorization": settings.API_KEY.get_secret_value()},
    )
    assert response.status_code == status.HTTP_200_OK
    user = response.json()
    assert user["name"] == name


def test_create_user(client: TestClient):
    user_data = {"name": "NewUser"}
    response = client.post(
        url="/users/",
        headers={"Authorization": settings.API_KEY.get_secret_value()},
        json=user_data,
    )
    assert response.status_code == status.HTTP_201_CREATED
    user = response.json()
    assert user["name"] == user_data["name"]


def test_create_user_invalid_data(client: TestClient):
    user_data = {"invalid_field": "NewUser"}
    response = client.post(
        url="/users/",
        headers={"Authorization": settings.API_KEY.get_secret_value()},
        json=user_data,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    error = response.json()
    assert "name" in error["detail"][0]
