from typing import Annotated

from api.deps import SessionDep, get_db_session
from excepts import DatabaseEntryNotFound, get_error_content
from fastapi import APIRouter, Depends, HTTPException, Query, status
from models import UUID7, Hero, HeroCreate, HeroPublic, HeroUpdate
from sqlmodel import select
from utils.log import get_logger

logger = get_logger()
router = APIRouter()


@router.post(
    path="/",
    summary="Create a new hero",
    status_code=status.HTTP_200_OK,
    response_description="Returns the created hero",
    response_model=HeroPublic,
    dependencies=[Depends(get_db_session)],
)
def create_hero(hero: HeroCreate, session: SessionDep):
    try:
        db_hero = Hero.model_validate(hero)
        session.add(db_hero)
        session.commit()
        session.refresh(db_hero)
        return db_hero
    except Exception as e:
        error = get_error_content(e)
        error_message = error.message

        logger.error(
            error_message,
            exc_info=True,
            stack_info=True,
        )

        session.rollback()

        raise HTTPException(
            status_code=error.http_status_code,
            detail=error_message,
        )


@router.get(
    path="/",
    summary="Retrieve a list of heroes",
    status_code=status.HTTP_200_OK,
    response_description="Returns a list of heroes",
    response_model=list[HeroPublic],
    dependencies=[Depends(get_db_session)],
)
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Hero]:
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return list(heroes)


@router.get(
    path="/{hero_id}",
    summary="Retrieve a hero by ID",
    status_code=status.HTTP_200_OK,
    response_description="Returns the hero with the specified ID",
    response_model=HeroPublic,
    dependencies=[Depends(get_db_session)],
)
def read_hero(hero_id: UUID7, session: SessionDep):
    try:
        hero = session.get(Hero, hero_id)
        if not hero:
            raise DatabaseEntryNotFound(f"Hero with ID {hero_id} not found")
        return hero
    except Exception as e:
        error = get_error_content(e)
        error_message = error.message

        logger.error(
            error_message,
            exc_info=True,
            stack_info=True,
        )

        session.rollback()

        raise HTTPException(
            status_code=error.http_status_code,
            detail=error_message,
        )


@router.patch(
    path="/{hero_id}",
    summary="Update a hero by ID",
    status_code=status.HTTP_200_OK,
    response_description="Returns the updated hero",
    response_model=HeroPublic,
    dependencies=[Depends(get_db_session)],
)
def update_hero(hero_id: UUID7, hero: HeroUpdate, session: SessionDep):
    try:
        hero_db = session.get(Hero, hero_id)
        if not hero_db:
            raise DatabaseEntryNotFound(f"Hero with ID {hero_id} not found")
        hero_data = hero.model_dump(exclude_unset=True)
        hero_db.sqlmodel_update(hero_data)
        session.add(hero_db)
        session.commit()
        session.refresh(hero_db)
        return hero_db
    except Exception as e:
        error = get_error_content(e)
        error_message = error.message

        logger.error(
            error_message,
            exc_info=True,
            stack_info=True,
        )

        session.rollback()

        raise HTTPException(
            status_code=error.http_status_code,
            detail=error_message,
        )


@router.delete(
    path="/{hero_id}",
    summary="Delete a hero by ID",
    status_code=status.HTTP_200_OK,
    response_description="Indicates whether the hero was successfully deleted",
    dependencies=[Depends(get_db_session)],
)
def delete_hero(hero_id: UUID7, session: SessionDep):
    try:
        hero = session.get(Hero, hero_id)
        if not hero:
            raise DatabaseEntryNotFound("Hero not found")
        session.delete(hero)
        session.commit()
        return {"ok": True}
    except Exception as e:
        error = get_error_content(e)
        error_message = error.message

        logger.error(
            error_message,
            exc_info=True,
            stack_info=True,
        )

        session.rollback()

        raise HTTPException(
            status_code=error.http_status_code,
            detail=error_message,
        )
