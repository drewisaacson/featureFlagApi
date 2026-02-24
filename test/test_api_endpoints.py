import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.inMemoryFeatureConfigDao import InMemoryFeatureConfigDao
from app.items.feature import Feature
from app.items.featureOverride import FeatureOverride


@pytest.fixture
def client_with_dao(tmp_path, monkeypatch):
    """Create a test client with an isolated DAO."""
    cache_file = tmp_path / "features.json"
    test_dao = InMemoryFeatureConfigDao(cache_file=str(cache_file))
    monkeypatch.setattr("app.main.dao", test_dao)
    return TestClient(app), test_dao


def test_get_feature_returns_200_with_feature(client_with_dao):
    """Test GET /feature/{feature_name} returns 200 with feature data."""
    client, dao = client_with_dao
    feature = Feature(
        feature_name="dummy",
        value="enabled",
    )
    dao.create_feature(feature)

    response = client.get("/feature/dummy")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["feature"]["feature_name"] == "dummy"


def test_get_feature_returns_404_when_missing(client_with_dao):
    """Test GET /feature/{feature_name} returns 404 when feature not found."""
    client, _ = client_with_dao
    response = client.get("/feature/nonexistent")
    assert response.status_code == 404
    assert "Feature nonexistent not found" in response.json()["detail"]


def test_get_feature_for_user_returns_200_with_override(
    client_with_dao,
):
    """
    Test GET /feature/{feature_name}/user/{user_id} returns 200 with override.
    """
    client, dao = client_with_dao
    feature = Feature(
        feature_name="dummy",
        value="enabled",
    )
    dao.create_feature(feature)

    override = FeatureOverride(
        feature_name="dummy",
        user_id="user_1",
        value="disabled",
    )
    dao.create_override("dummy", override)

    response = client.get("/feature/dummy/user/user_1")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["override"]["user_id"] == "user_1"


def test_get_feature_for_user_returns_200_with_default_value(
    client_with_dao,
):
    """
    Test GET /feature/{feature_name}/user/{user_id} returns 200 with default.
    """
    client, dao = client_with_dao
    feature = Feature(
        feature_name="dummy",
        value="enabled",
    )
    dao.create_feature(feature)

    response = client.get("/feature/dummy/user/nonexistent")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["override"]["value"] == "enabled"


def test_get_feature_for_user_returns_404_when_feature_missing(
    client_with_dao,
):
    """
    Test GET /feature/{feature_name}/user/{user_id} returns 404 when missing.
    """
    client, _ = client_with_dao
    response = client.get("/feature/nonexistent/user/user_1")
    assert response.status_code == 404
    assert "Feature nonexistent not found" in response.json()["detail"]
