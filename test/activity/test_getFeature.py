from app.activity.getFeature import get_feature
from app.db.inMemoryFeatureConfigDao import InMemoryFeatureConfigDao
from app.items.feature import Feature


def test_get_feature_returns_feature(tmp_path):
    cache_file = tmp_path / "features.json"
    dao = InMemoryFeatureConfigDao(cache_file=str(cache_file))

    feature = Feature(
        feature_name="dummy",
        value="enabled",
    )
    dao.create_feature(feature)

    retrieved = get_feature("dummy", dao)
    assert retrieved.feature_name == "dummy"
    assert retrieved.value == "enabled"


def test_get_feature_missing_raises_error(tmp_path):
    cache_file = tmp_path / "features.json"
    dao = InMemoryFeatureConfigDao(cache_file=str(cache_file))

    try:
        get_feature("dummy", dao)
    except ValueError as exc:
        assert str(exc) == "Feature not found"
    else:
        assert False, "Expected ValueError when feature is missing"
