import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db
from app.models.pokemon_db import PokemonDB  # noqa: F401

# Cria um banco de dados SQLite na memória RAM (temporário)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def test_db():
    # Cria as tabelas no banco em memória
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Destrói as tabelas após o teste
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(test_db):
    # Força a API a usar o banco de teste no lugar do banco real
    def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    # Limpa a substituição depois do teste
    app.dependency_overrides.clear()
