import time
from datetime import datetime

from app.db.cachedFeatureConfigDao import CachedFeatureConfigDao
from app.db.inMemoryFeatureConfigDao import InMemoryFeatureConfigDao
from app.items.feature import Feature
from app.items.featureOverride import FeatureOverride


def test_cache_returns_cached_feature(tmp_path):
    """Test that cached feature is returned without hitting base DAO."""
    cache_file = tmp_path / "features.json"
    base_dao = InMemoryFeatureConfigDao(cache_file=str(cache_file))
    cached_dao = CachedFeatureConfigDao(base_dao, ttl_seconds=300)

    feature = Feature(
        feature_name="dummy",
        value="enabled",
        timestamp=datetime.now(),
    )
    base_dao.create_feature(feature)

    retrieved1 = cached_dao.get_feature("dummy")
    assert retrieved1 is not None

    modified = Feature(
        feature_name="dummy",
        value="disabled",
        timestamp=datetime.now(),
    )
    base_dao.features["dummy"] = modified

    retrieved2 = cached_dao.get_feature("dummy")
    assert retrieved2.value == "enabled"


def test_cache_expires_after_ttl(tmp_path):
    """Test that cache entries expire after TTL."""
    cache_file = tmp_path / "features.json"
    base_dao = InMemoryFeatureConfigDao(cache_file=str(cache_file))
    cached_dao = CachedFeatureConfigDao(base_dao, ttl_seconds=1)

    feature = Feature(
        feature_name="dummy",
        value="enabled",
        timestamp=datetime.now(),
    )
    base_dao.create_feature(feature)

    retrieved1 = cached_dao.get_feature("dummy")
    assert retrieved1.value == "enabled"

    time.sleep(1.1)

    modified = Feature(
        feature_name="dummy",
        value="disabled",
        timestamp=datetime.now(),
    )
    base_dao.features["dummy"] = modified

    retrieved2 = cached_dao.get_feature("dummy")
    assert retrieved2.value == "disabled"


def test_cache_invalidates_on_create_feature(tmp_path):
    """Test that creating a feature invalidates its cache."""
    cache_file = tmp_path / "features.json"
    base_dao = InMemoryFeatureConfigDao(cache_file=str(cache_file))
    cached_dao = CachedFeatureConfigDao(base_dao, ttl_seconds=300)

    feature1 = Feature(
        feature_name="dummy",
        value="enabled",
        timestamp=datetime.now(),
    )
    cached_dao.create_feature(feature1)

    retrieved1 = cached_dao.get_feature("dummy")
    assert retrieved1.value == "enabled"

    feature2 = Feature(
        feature_name="dummy",
        value="disabled",
        timestamp=datetime.now(),
    )
    cached_dao.create_feature(feature2)

    retrieved2 = cached_dao.get_feature("dummy")
    assert retrieved2.value == "disabled"


def test_cache_handles_missing_feature(tmp_path):
    """Test that missing features are handled correctly."""
    cache_file = tmp_path / "features.json"
    base_dao = InMemoryFeatureConfigDao(cache_file=str(cache_file))
    cached_dao = CachedFeatureConfigDao(base_dao, ttl_seconds=300)

    result = cached_dao.get_feature("missing")
    assert result is None


def test_cache_invalidates_on_create_override(tmp_path):
    """Test that creating an override invalidates its cache."""
    cache_file = tmp_path / "features.json"
    base_dao = InMemoryFeatureConfigDao(cache_file=str(cache_file))
    cached_dao = CachedFeatureConfigDao(base_dao, ttl_seconds=300)

    feature = Feature(
        feature_name="dummy",
        value="enabled",
        timestamp=datetime.now(),
    )
    base_dao.create_feature(feature)

    override1 = FeatureOverride(
        feature_name="dummy",
        user_id="user_1",
        value="disabled",
        timestamp=datetime.now(),
    )
    cached_dao.create_override("dummy", override1)

    retrieved1 = cached_dao.get_override("dummy", "user_1")
    assert retrieved1.value == "disabled"

    override2 = FeatureOverride(
        feature_name="dummy",
        user_id="user_1",
        value="enabled",
        timestamp=datetime.now(),
    )
    cached_dao.create_override("dummy", override2)

    retrieved2 = cached_dao.get_override("dummy", "user_1")
    assert retrieved2.value == "enabled"


def test_cache_invalidates_on_delete_override(tmp_path):
    """Test that deleting an override invalidates its cache."""
    cache_file = tmp_path / "features.json"
    base_dao = InMemoryFeatureConfigDao(cache_file=str(cache_file))
    cached_dao = CachedFeatureConfigDao(base_dao, ttl_seconds=300)

    feature = Feature(
        feature_name="dummy",
        value="enabled",
        timestamp=datetime.now(),
    )
    base_dao.create_feature(feature)

    override = FeatureOverride(
        feature_name="dummy",
        user_id="user_1",
        value="disabled",
        timestamp=datetime.now(),
    )
    cached_dao.create_override("dummy", override)

    retrieved = cached_dao.get_override("dummy", "user_1")
    assert retrieved is not None

    cached_dao.delete_override("dummy", "user_1")

    result = cached_dao.get_override("dummy", "user_1")
    assert result is None
