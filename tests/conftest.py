import os
import tempfile
from pathlib import Path

import pytest
from api.deps import get_db_session
from database import create_db_and_tables
from main import app
from sqlmodel import Session, create_engine
from starlette.testclient import TestClient


@pytest.fixture
def data_folder_path():
    return Path(__file__).parent.parent / "data"


@pytest.fixture(name="session")
def session_fixture() -> Session:
    """Create an engine with all migrations applied."""
    # Create a temporary database file
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    db_url = f"sqlite:///{path}"

    # Get path to alembic.ini
    # package_dir = Path(product_serving.__file__).parent
    # alembic_ini_path = package_dir / "alembic.ini"

    # Create Alembic config and run migrations
    # config = Config(str(alembic_ini_path))
    # config.set_main_option("sqlalchemy.url", db_url)
    # command.upgrade(config, "head")

    engine = create_engine(db_url)
    # TODO: Alternatively, you can create tables directly without migrations for simpler setups.
    create_db_and_tables(engine)
    with Session(engine) as session:
        yield session

    # Clean up
    engine.dispose()
    os.unlink(path)


@pytest.fixture(name="client_with_db")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_db_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
