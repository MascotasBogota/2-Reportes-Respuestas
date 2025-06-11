import pytest
from app import create_app
from src.extensions import init_db
from mongoengine import disconnect


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    init_db(app)
    yield app
    disconnect()  # cerrar conexión a Mongo luego del test


@pytest.fixture
def client(app):
    return app.test_client()