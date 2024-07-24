import os
import pathlib

import pytest
from dotenv import load_dotenv
from starlette.testclient import TestClient

from main import create_app
from routers.cart import get_config


@pytest.fixture(scope="function")
def client(request):
    app = create_app()

    # Apply dependency overrides if provided
    overrides = getattr(request, "param", {})
    for dependency, override_function in overrides.items():
        app.dependency_overrides[get_config] = override_function

    with TestClient(app) as client:
        yield client

    app.dependency_overrides = {}
