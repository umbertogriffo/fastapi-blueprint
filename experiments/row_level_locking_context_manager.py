# Here's how to implement a basic transaction pattern that uses row-level locking to prevent write collisions.
# The with_for_update() call ensures that other transactions must wait until the current transaction completes before they can modify the same row.
# The flag_modified is only needed for JSON columns since sqlmodel doesn't detect changes automatically to changes in the dicts!
# Note: SQLite doesn't support row-level locking, so these parameters won't have effect. Consider PostgreSQL or MySQL for production use.

from contextlib import contextmanager

from models import Hero
from sqlmodel import Session, SQLModel, create_engine, select


@contextmanager
def lock_hero_and_update(engine, hero_id: int):
    """
    Context manager that locks a task row for exclusive access and updates it.
    """
    with Session(engine) as session:
        try:
            # Lock the task row for exclusive access
            statement = select(Hero).where(Hero.id == hero_id).with_for_update()
            hero = session.exec(statement).one()
            yield hero
            # Validate and mark the hero as modified
            Hero.model_validate(hero)
            # flag_modified(hero, "output")
            session.add(hero)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e


if __name__ == "__main__":
    engine = create_engine("postgresql://develop:develop_secret@localhost:5432/develop")
    SQLModel.metadata.create_all(engine)

    # Create test hero
    with Session(engine) as session:
        hero_sample = Hero(name="Spider-Man", age=25, secret_name="Peter Parker")
        session.add(hero_sample)
        session.commit()
        session.refresh(hero_sample)
        hero_id = hero_sample.id

    with lock_hero_and_update(engine, hero_id) as hero:
        hero.age = 41
