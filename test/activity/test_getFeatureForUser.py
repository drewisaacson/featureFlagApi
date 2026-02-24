from app.activity.getFeatureForUser import get_feature_for_user
from app.db.inMemoryFeatureConfigDao import InMemoryFeatureConfigDao
from app.items.feature import Feature
from app.items.featureOverride import FeatureOverride


def test_get_feature_for_user_returns_override(tmp_path):
    cache_file = tmp_path / "features.json"
    dao = InMemoryFeatureConfigDao(cache_file=str(cache_file))

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

    retrieved = get_feature_for_user("dummy", "user_1", dao)
    assert retrieved.feature_name == "dummy"
    assert retrieved.user_id == "user_1"
    assert retrieved.value == "disabled"
    assert retrieved.isDefault is False


def test_get_feature_for_user_missing_override_returns_default(tmp_path):
    cache_file = tmp_path / "features.json"
    dao = InMemoryFeatureConfigDao(cache_file=str(cache_file))

    feature = Feature(
        feature_name="dummy",
        value="enabled",
    )
    dao.create_feature(feature)

    retrieved = get_feature_for_user("dummy", "user_1", dao)
    assert retrieved.feature_name == "dummy"
    assert retrieved.user_id == "user_1"
    assert retrieved.value == "enabled"
    assert retrieved.isDefault is True


def test_get_feature_for_user_missing_feature_raises_error(tmp_path):
    cache_file = tmp_path / "features.json"
    dao = InMemoryFeatureConfigDao(cache_file=str(cache_file))

    try:
        get_feature_for_user("dummy", "user_1", dao)
    except ValueError as exc:
        assert str(exc) == "Feature dummy not found"
    else:
        assert False, "Expected ValueError when feature is missing"
