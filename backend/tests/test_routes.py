from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_read_status():
    response = client.get("/api/status")
    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "game": "kleurenwiezen",
        "version": "1.0.0"
    }
