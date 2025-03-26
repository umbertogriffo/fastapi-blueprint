import pytest
from pydantic import ValidationError
from schemas import User


def test_valid_user_creation():
    user_data = {"name": "TestUser"}
    user = User(**user_data)
    assert user.name == "TestUser"
    assert user.model_dump() == user_data


def test_user_missing_name():
    with pytest.raises(ValidationError) as exc_info:
        User()

    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0]["type"] == "missing"
    assert errors[0]["loc"] == ("name",)


def test_user_empty_name():
    with pytest.raises(ValidationError) as exc_info:
        User(name="")

    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0]["type"] == "string_too_short"


def test_user_invalid_type():
    with pytest.raises(ValidationError):
        User(name=123)
