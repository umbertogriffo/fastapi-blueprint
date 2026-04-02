# Rollback when using pytest

When using `pytest` with SQLModel and a database, it's important to ensure that changes made during tests do not persist and affect other tests.

Here are some strategies to achieve this:

In `conftest.py` create a session that rolls back after each test:
```python
    # Start a transaction that will be rolled back after the test
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    # Rollback all changes made during the test
    session.close()
    transaction.rollback()
    connection.close()
```

Or [use a nested transaction for better test isolation](https://github.com/fastapi/sqlmodel/discussions/940):
```python
import sqlalchemy as sa
from sqlmodel import Session

    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    nested = connection.begin_nested()

    @sa.event.listens_for(session, "after_transaction_end")
    def end_savepoint(session, transaction):
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield session

    session.close()
    transaction.rollback()
    connection.close()
```

or recreate the entire database schema between tests (recreating the schema is slow):
```python
    with Session(engine) as session:
        yield session

    # For Postgres, clean up all data between tests
    if db_type == "postgres":
        command.downgrade(config, "base")
```
