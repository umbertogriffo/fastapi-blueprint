from pathlib import Path

import pytest
import sqlalchemy as sa
from alembic import command
from alembic.config import Config
from api.deps import get_db_session
from main import app
from sqlmodel import Session, create_engine
from starlette.testclient import TestClient


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--db",
        action="store",
        default="sqlite",
        choices=["sqlite", "postgres"],
        help="Database to use for tests: sqlite (default) or postgres",
    )


@pytest.fixture
def data_folder_path():
    return Path(__file__).parent.parent / "data"


@pytest.fixture(scope="session")
def db_engine(request, tmp_path_factory, session_mocker):
    """
    Create a session-scoped database engine.
    Database is created once and migrations run once for all tests.
    """
    # TODO: Use an in-memory SQLite database for faster tests if possible.
    #       https://sqlmodel.tiangolo.com/tutorial/fastapi/tests/#memory-database

    db_type = request.config.getoption("--db")
    if db_type == "postgres":
        db_url = "postgresql://develop:develop_secret@localhost:5432/develop"
    else:
        # Create a temporary database file for SQLite
        temp_dir = tmp_path_factory.mktemp("db")
        db_path = temp_dir / "test.db"
        db_url = f"sqlite:///{db_path}"

    # Use monkeypatch to set DATABASE_URL environment variable
    session_mocker.patch("config.settings.DATABASE_URL", db_url)

    # Get path to alembic.ini
    src_dir = Path(__file__).parents[1] / "src"
    alembic_ini_path = src_dir / "alembic.ini"

    # Create Alembic config and run migrations
    config = Config(str(alembic_ini_path))
    config.set_main_option("sqlalchemy.url", db_url)
    command.upgrade(config, "head")

    engine = create_engine(db_url)
    # TODO: Alternatively, you can create tables directly without migrations for simpler setups.
    # create_db_and_tables(engine)

    yield engine

    # Clean up at the end of the test session
    engine.dispose()


@pytest.fixture(name="session")
def session_fixture(db_engine) -> Session:
    """
    Create a new database session for a test, wrapped in a transaction that is rolled back after the test.
    """

    connection = db_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    # Ensure that changes made during tests do not persist and affect other tests using a nested transaction
    nested = connection.begin_nested()

    @sa.event.listens_for(session, "after_transaction_end")
    def end_savepoint(session, transaction):
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield session

    # Rollback the transaction (this undoes all changes made during the test)
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(name="client_with_db")
def client_fixture(session: Session):
    """Create a TestClient that uses the test database session."""

    def get_session_override():
        return session

    app.dependency_overrides[get_db_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
