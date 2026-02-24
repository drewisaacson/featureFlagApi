from app.activity.deleteFeatureForUser import delete_feature_for_user
from app.db.inMemoryFeatureConfigDao import InMemoryFeatureConfigDao
from app.items.feature import Feature
from app.items.featureOverride import FeatureOverride


def test_delete_feature_for_user_removes_override(tmp_path):
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

    deleted = delete_feature_for_user("dummy", "user_1", dao)
    assert deleted.feature_name == "dummy"
    assert deleted.user_id == "user_1"
    assert dao.get_override("dummy", "user_1") is None


def test_delete_feature_for_user_missing_feature_raises_error(tmp_path):
    cache_file = tmp_path / "features.json"
    dao = InMemoryFeatureConfigDao(cache_file=str(cache_file))

    try:
        delete_feature_for_user("dummy", "user_1", dao)
    except ValueError as exc:
        assert str(exc) == "Feature dummy not found"
    else:
        assert False, "Expected ValueError when feature is missing"


def test_delete_feature_for_user_missing_override_raises_error(tmp_path):
    cache_file = tmp_path / "features.json"
    dao = InMemoryFeatureConfigDao(cache_file=str(cache_file))

    feature = Feature(
        feature_name="dummy",
        value="enabled",
    )
    dao.create_feature(feature)

    try:
        delete_feature_for_user("dummy", "user_1", dao)
    except ValueError as exc:
        assert (
            str(exc)
            == "Override for feature dummy and user user_1 not found"
        )
    else:
        assert False, "Expected ValueError when override is missing"
