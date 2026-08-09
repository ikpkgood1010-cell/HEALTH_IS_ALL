from fastapi.testclient import TestClient
from backend.main import app

def test_database_missing_is_safe():
    client = TestClient(app)
    assert client.get("/readyz").json() == {"status": "not_ready", "database": "not_configured"}
    assert client.get("/api/v1/health-i/status/user").status_code == 503
