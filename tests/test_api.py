import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import AsyncMock, patch

client = TestClient(app)

# Mock Redis to avoid needing a running Redis instance for tests
@pytest.fixture(autouse=True)
def mock_redis():
    with patch("app.service.kundli_service.CacheService") as MockCache:
        mock_instance = MockCache.return_value
        mock_instance.get = AsyncMock(return_value=None)
        mock_instance.set = AsyncMock()
        yield mock_instance

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_generate_kundli():
    payload = {
        "dob": "1989-02-24",
        "tob": "16:30:00",
        "timezone": 5.5,
        "lat": 28.5355,
        "lon": 77.3910,
        "ayanamsa": 1
    }
    
    response = client.post("/api/v1/kundli/generate", json=payload)
    assert response.status_code == 200, f"Request failed: {response.text}"
    data = response.json()
    
    assert "lagna" in data
    assert "planets" in data
    assert len(data["planets"]) >= 9
    assert "houses" in data
    assert len(data["houses"]) == 12
    
    assert "dasha" in data
    assert "mahadashas" in data["dasha"]
    assert len(data["dasha"]["mahadashas"]) > 0
    
    # Check Antardasha
    first_md = data["dasha"]["mahadashas"][0]
    assert "sub_periods" in first_md
    assert len(first_md["sub_periods"]) > 0
