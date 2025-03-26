from typing import List

from fastapi import APIRouter
from schemas import User
from starlette import status

router = APIRouter()


@router.get(
    path="/",
    summary="Retrieve a list of users",
    status_code=status.HTTP_200_OK,
    response_description="Returns a list of users",
    response_model=List[User],
)
async def read_users():
    return [User(name="Rick"), User(name="Morty")]


@router.get(
    path="/me",
    summary="Retrieve the current user",
    status_code=status.HTTP_200_OK,
    response_description="Returns the current user",
    response_model=User,
)
async def read_user_me():
    return User(name="Fra")


@router.get(
    path="/{name}",
    summary="Retrieve a user by name",
    status_code=status.HTTP_200_OK,
    response_description="Returns the user with the specified name",
    response_model=User,
)
async def read_user(name: str):
    return User(name=name)


@router.post(
    path="/",
    summary="Create a new user",
    status_code=status.HTTP_201_CREATED,
    response_description="Returns the created user",
    response_model=User,
)
async def create_user(user: User):
    return user
