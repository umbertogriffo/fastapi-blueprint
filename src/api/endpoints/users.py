from typing import List

from api.deps import api_key_auth
from excepts import InvalidValue, get_error_content
from fastapi import APIRouter, Depends, HTTPException
from schemas import User
from starlette import status
from utils.log import get_logger

logger = get_logger()
router = APIRouter()


@router.get(
    path="/",
    summary="Retrieve a list of users",
    status_code=status.HTTP_200_OK,
    response_description="Returns a list of users",
    response_model=List[User],
    dependencies=[Depends(api_key_auth)],
)
async def read_users():
    return [User(name="Rick"), User(name="Morty")]


@router.get(
    path="/me",
    summary="Retrieve the current user",
    status_code=status.HTTP_200_OK,
    response_description="Returns the current user",
    response_model=User,
    dependencies=[Depends(api_key_auth)],
)
async def read_user_me():
    return User(name="Umberto")


@router.get(
    path="/{name}",
    summary="Retrieve a user by name",
    status_code=status.HTTP_200_OK,
    response_description="Returns the user with the specified name",
    response_model=User,
    dependencies=[Depends(api_key_auth)],
)
async def read_user(name: str):
    logger.info(f"User Name: {name}")
    return User(name=name)


@router.post(
    path="/",
    summary="Create a new user",
    status_code=status.HTTP_201_CREATED,
    response_description="Returns the created user",
    response_model=User,
    dependencies=[Depends(api_key_auth)],
)
async def create_user(user: User):
    return user


@router.post(
    path="/check",
    summary="Create a user with validation",
    status_code=status.HTTP_201_CREATED,
    response_description="Returns the created user or error",
    response_model=User,
    dependencies=[Depends(api_key_auth)],
)
async def create_user_with_check(user: User):
    try:
        if user.name.lower() == "admin":
            raise InvalidValue("Username 'admin' is reserved")

        return user

    except Exception as e:
        error = get_error_content(e)
        error_message = error.message

        logger.error(
            error_message,
            exc_info=True,
            stack_info=True,
        )

        raise HTTPException(
            status_code=error.http_status_code,
            detail=error_message,
        )
