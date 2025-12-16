from typing import Annotated, Generator

from config import settings
from database import engine
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from sqlmodel import Session
from starlette import status

"""
Defines dependencies used by the endpoints.
"""


def get_db_session() -> Generator[Session, None, None]:
    """
    Create a new database session and close the session after the operation has ended.
    """
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db_session)]


def api_key_auth(api_key: str = Depends(APIKeyHeader(name="Authorization"))) -> None:
    # Validate the provided API key
    if api_key != settings.API_KEY.get_secret_value():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key"
        )
