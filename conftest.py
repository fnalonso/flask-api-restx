import pytest
from src.app import create_app


@pytest.fixture
def client():
    app = create_app()
    # app.config['SERVER_NAME'] = "localhost:5000"
    app.url_map.strict_slashes = False
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def user_data():
    return dict(
        username="maradona",
        password="123mudar"
    )