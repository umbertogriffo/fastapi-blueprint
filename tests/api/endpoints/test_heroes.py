from fastapi import status
from models import Hero
from sqlmodel import Session
from starlette.testclient import TestClient


def test_create_hero(client_with_db: TestClient, session: Session):
    response = client_with_db.post(
        "/heroes/", json={"name": "Deadpond", "secret_name": "Dive Wilson"}
    )

    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data["name"] == "Deadpond"
    assert data["age"] is None
    assert data["id"] is not None


def test_create_hero_incomplete(client: TestClient):
    # No secret_name
    response = client.post("/heroes/", json={"name": "Deadpond"})
    assert response.status_code == 422


def test_create_hero_invalid(client: TestClient):
    # secret_name has an invalid type
    response = client.post(
        "/heroes/",
        json={
            "name": "Deadpond",
            "secret_name": {"message": "Do you wanna know my secret identity?"},
        },
    )
    assert response.status_code == 422


def test_read_heroes(session: Session, client_with_db: TestClient):
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)
    session.add(hero_1)
    session.add(hero_2)
    session.commit()

    response = client_with_db.get("/heroes/")
    data = response.json()

    assert response.status_code == 200

    assert len(data) == 2
    assert data[0]["name"] == hero_1.name
    assert "secret_name" not in data[0].keys()
    assert data[0]["age"] == hero_1.age
    assert data[0]["id"] == str(hero_1.id)
    assert data[1]["name"] == hero_2.name
    assert "secret_name" not in data[1].keys()
    assert data[1]["age"] == hero_2.age
    assert data[1]["id"] == str(hero_2.id)


def test_read_hero(session: Session, client_with_db: TestClient):
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    session.add(hero_1)
    session.commit()

    response = client_with_db.get(f"/heroes/{hero_1.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == hero_1.name
    assert "secret_name" not in data.keys()
    assert data["age"] == hero_1.age
    assert data["id"] == str(hero_1.id)


def test_update_hero(session: Session, client_with_db: TestClient):
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    session.add(hero_1)
    session.commit()

    response = client_with_db.patch(f"/heroes/{hero_1.id}", json={"name": "Deadpuddle"})
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Deadpuddle"
    assert "secret_name" not in data.keys()
    assert data["age"] is None
    assert data["id"] == str(hero_1.id)


def test_delete_hero(session: Session, client_with_db: TestClient):
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    session.add(hero_1)
    session.commit()

    response = client_with_db.delete(f"/heroes/{hero_1.id}")

    hero_in_db = session.get(Hero, hero_1.id)

    assert response.status_code == 200
    assert hero_in_db is None


def test_update_hero_rollback_on_error(
    mocker, client_with_db: TestClient, session: Session
):
    """Test that updating a hero rolls back on commit error."""
    hero = Hero(name="Deadpond", secret_name="Dive Wilson")
    session.add(hero)
    session.commit()

    with mocker.patch.object(session, "commit", side_effect=Exception("Commit failed")):
        response = client_with_db.patch(f"/heroes/{hero.id}", json={"name": "NewName"})

        assert "Commit failed" in response.text
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

        # Verify hero wasn't updated
        session.refresh(hero)
        assert hero.name == "Deadpond"
