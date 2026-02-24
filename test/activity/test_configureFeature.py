from app.activity.configureFeature import configure_feature
from app.db.inMemoryFeatureConfigDao import InMemoryFeatureConfigDao
from app.items.feature import Feature


def test_configure_feature_sets_timestamp(tmp_path):
    cache_file = tmp_path / "features.json"
    dao = InMemoryFeatureConfigDao(cache_file=str(cache_file))

    feature = Feature(
        feature_name="dummy",
        value="enabled",
    )

    created = configure_feature(feature, dao)

    assert created.timestamp is not None


def test_configure_feature_persists_feature(tmp_path):
    cache_file = tmp_path / "features.json"
    dao = InMemoryFeatureConfigDao(cache_file=str(cache_file))

    feature = Feature(
        feature_name="dummy",
        value="enabled",
    )

    configure_feature(feature, dao)

    stored = dao.get_feature("dummy")
    assert stored is not None
    assert stored.feature_name == "dummy"
    assert stored.value == "enabled"
