from datetime import datetime

from app.db.inMemoryFeatureConfigDao import InMemoryFeatureConfigDao
from app.items.feature import Feature
from app.items.featureOverride import FeatureOverride


def test_create_and_get_feature(tmp_path):
    cache_file = tmp_path / "features.json"
    dao = InMemoryFeatureConfigDao(cache_file=str(cache_file))

    feature = Feature(
        feature_name="dummy",
        value="enabled",
        feature_description="Enable new UI",
        timestamp=datetime(2024, 1, 1, 12, 0, 0),
    )
    created = dao.create_feature(feature)

    fetched = dao.get_feature("dummy")
    assert created == fetched


def test_create_and_get_override(tmp_path):
    cache_file = tmp_path / "features.json"
    dao = InMemoryFeatureConfigDao(cache_file=str(cache_file))

    override = FeatureOverride(
        feature_name="dummy",
        user_id="user_1",
        value="disabled",
        justification="A/B test",
        timestamp=datetime(2024, 1, 2, 9, 30, 0),
    )
    created = dao.create_override("dummy", override)

    fetched = dao.get_override("dummy", "user_1")
    assert created == fetched


def test_delete_override(tmp_path):
    cache_file = tmp_path / "features.json"
    dao = InMemoryFeatureConfigDao(cache_file=str(cache_file))

    override = FeatureOverride(
        feature_name="dummy",
        user_id="user_2",
        value="enabled",
        timestamp=datetime(2024, 1, 3, 10, 0, 0),
    )
    dao.create_override("dummy", override)

    deleted = dao.delete_override("dummy", "user_2")
    assert deleted is not None
    assert dao.get_override("dummy", "user_2") is None


def test_load_from_file_persists_features_and_overrides(tmp_path):
    cache_file = tmp_path / "features.json"
    dao = InMemoryFeatureConfigDao(cache_file=str(cache_file))

    feature = Feature(
        feature_name="dummy",
        value="enabled",
        timestamp=datetime(2024, 2, 1, 8, 0, 0),
    )
    override = FeatureOverride(
        feature_name="dummy",
        user_id="user_3",
        value="disabled",
        timestamp=datetime(2024, 2, 1, 8, 5, 0),
    )

    dao.create_feature(feature)
    dao.create_override("dummy", override)

    reloaded = InMemoryFeatureConfigDao(cache_file=str(cache_file))

    assert reloaded.get_feature("dummy") is not None
    assert reloaded.get_override("dummy", "user_3") is not None


def test_corrupted_cache_file_is_ignored(tmp_path):
    cache_file = tmp_path / "features.json"
    cache_file.write_text("{\n  \"features\": [\n")

    dao = InMemoryFeatureConfigDao(cache_file=str(cache_file))

    assert dao.get_feature("dummy") is None
    assert dao.get_override("dummy", "user") is None
