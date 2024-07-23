import os
import pathlib

import pytest
from dotenv import load_dotenv
from starlette.testclient import TestClient

from main import create_app


@pytest.fixture(scope="function")
def client():
    app = create_app()

    with TestClient(app) as client:
        yield client
