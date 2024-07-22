import os
import pathlib

import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from src.database import Base, get_db
from src.main import create_app

load_dotenv(dotenv_path=pathlib.Path(__file__).parent.resolve())

# Conexão com banco Postgres através da lib sqlalchemy
engine = create_engine(os.environ.get("SQLALCHEMY_TEST_DATABASE_URL"))
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def test_db():
    Base.metadata.create_all(bind=engine)  # Cria tabela
    yield
    Base.metadata.drop_all(bind=engine)  # Apaga tabela


@pytest.fixture(scope="function")
def db_session(test_db):
    connection = engine.connect()
    transaction = connection.begin()
    session = TestSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    app = create_app()

    # Override the get_db dependency to use the test database session
    app.dependency_overrides[get_db] = lambda: db_session

    with TestClient(app) as client:
        yield client
