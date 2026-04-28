import pytest
from app import app as flask_app 

@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client

def test_app_starts(client):
    # Al realizar cualquier petición, pytest "pasa" por las líneas de app.py
    response = client.get('/api/test')
    assert response.status_code == 200