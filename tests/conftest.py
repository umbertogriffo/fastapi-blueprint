from pathlib import Path

import pytest
from main import app
from starlette.testclient import TestClient


@pytest.fixture
def data_folder_path():
    return Path(__file__).parent.parent / "data"


@pytest.fixture
def client(monkeypatch) -> TestClient:
    return TestClient(app)
