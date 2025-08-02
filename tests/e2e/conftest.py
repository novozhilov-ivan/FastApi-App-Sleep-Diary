import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.main import create_app


@pytest.fixture(scope="session")
def app() -> FastAPI:
    app = create_app()
    return app


@pytest.fixture(scope="session")
def client(app: FastAPI) -> TestClient:
    return TestClient(app)
