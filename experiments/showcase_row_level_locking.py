import threading
import time

from models import UUID7, Hero
from sqlalchemy import Engine
from sqlmodel import Session, create_engine, select


def update_without_lock(engine: Engine, hero_id: UUID7, new_age: int, delay: float):
    with Session(engine) as session:
        try:
            hero = session.get(Hero, hero_id)
            time.sleep(delay)  # Simulate processing time
            hero.age = new_age
            session.add(hero)
            session.commit()
            session.refresh(hero)
            print(f"✅ Updated without lock: new_age={new_age} updated_age={hero.age}")
        except Exception as e:
            session.rollback()
            print(f"❌ Updated without lock: new_age={new_age} failed - {e} \n")


def update_with_lock(
    engine: Engine,
    hero_id: UUID7,
    new_age: int,
    delay: float,
    nowait: bool = False,
    skip_locked: bool = False,
):
    with Session(engine) as session:
        try:
            statement = (
                select(Hero)
                .where(Hero.id == hero_id)
                .with_for_update(nowait=nowait, skip_locked=skip_locked)
            )
            hero = session.exec(statement).one()
            time.sleep(delay)  # Simulate processing time
            hero.age = new_age
            session.add(hero)
            session.commit()
            session.refresh(hero)
            print(f"✅ Updated with lock: age={new_age} updated_age={hero.age}")
        except Exception as e:
            session.rollback()
            print(f"❌ Updated without lock: new_age={new_age} failed - {e} \n")


def concurrent_update_test():
    """
    Simulates two concurrent transactions trying to update the same hero.
    Without with_for_update(), this could lead to lost updates.
    With it, the second transaction waits until the first commits.
    """
    engine = create_engine("postgresql://develop:develop_secret@localhost:5432/develop")

    # Create test hero
    with Session(engine) as session:
        hero = Hero(name="Spider-Man", age=25, secret_name="Peter Parker")
        session.add(hero)
        session.commit()
        session.refresh(hero)
        hero_id = hero.id

    # Demonstrate race condition without lock
    print("\n" + "=" * 60)
    print("Without lock (race condition possible):")
    print("=" * 60)
    threads = [
        threading.Thread(target=update_without_lock, args=(engine, hero_id, 26, 0.5)),
        threading.Thread(target=update_without_lock, args=(engine, hero_id, 27, 0.5)),
        threading.Thread(target=update_without_lock, args=(engine, hero_id, 30, 0.5)),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # Verify final age (demonstrates lost update)
    with Session(engine) as session:
        hero = session.get(Hero, hero_id)
        print(f"Final age without lock: {hero.age}")

    # Demonstrate safe concurrent access with Basic Row Locking
    print("\n" + "=" * 60)
    print("With lock (All false):")
    print("=" * 60)
    threads = [
        threading.Thread(target=update_with_lock, args=(engine, hero_id, 26, 0.5)),
        threading.Thread(target=update_with_lock, args=(engine, hero_id, 27, 0.5)),
        threading.Thread(target=update_with_lock, args=(engine, hero_id, 30, 0.5)),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # Verify final age (no lost update)
    with Session(engine) as session:
        hero = session.get(Hero, hero_id)
        print(f"Final age with lock: {hero.age}")

    # Demonstrate safe concurrent access with Fail Fast with nowait Locking
    # This raises an exception if another transaction holds the lock, allowing you to handle it gracefully.
    print("\n" + "=" * 60)
    print("With lock (nowait):")
    print("=" * 60)
    threads = [
        threading.Thread(
            target=update_with_lock, args=(engine, hero_id, 26, 0.5, True)
        ),
        threading.Thread(
            target=update_with_lock, args=(engine, hero_id, 27, 0.5, True)
        ),
        threading.Thread(
            target=update_with_lock, args=(engine, hero_id, 30, 0.5, True)
        ),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # Verify final age (no lost update)
    with Session(engine) as session:
        hero = session.get(Hero, hero_id)
        print(f"Final age with lock: {hero.age}")

    # Demonstrate safe concurrent access with Skip Locked Rows with skip_locked Locking
    # This skips rows that are locked by other transactions, allowing you to process other available rows.
    print("\n" + "=" * 60)
    print("With lock (skip_locked):")
    print("=" * 60)

    threads = [
        threading.Thread(
            target=update_with_lock, args=(engine, hero_id, 26, 0.5, False, True)
        ),
        threading.Thread(
            target=update_with_lock, args=(engine, hero_id, 27, 0.5, False, True)
        ),
        threading.Thread(
            target=update_with_lock, args=(engine, hero_id, 30, 0.5, False, True)
        ),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # Verify final age (no lost update)
    with Session(engine) as session:
        hero = session.get(Hero, hero_id)
        print(f"Final age with lock: {hero.age}")


if __name__ == "__main__":
    concurrent_update_test()
