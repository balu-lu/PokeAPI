import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    # O TestClient permite fazer requisições HTTP para a nossa API sem precisar subir o servidor
    return TestClient(app)
