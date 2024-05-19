import pytest
import httpx
from app.services import EnergyDataService
from fastapi.testclient import TestClient
from app.main import create_app

@pytest.fixture
def app():
    return create_app()

@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)

@pytest.fixture
def mock_energy_service():
    return EnergyDataService(httpx.AsyncClient())
