from app.activity.configureFeatureForUser import configure_feature_for_user
from app.db.inMemoryFeatureConfigDao import InMemoryFeatureConfigDao
from app.items.feature import Feature
from app.items.featureOverride import FeatureOverride


def test_configure_feature_for_user_missing_feature_raises(tmp_path):
    cache_file = tmp_path / "features.json"
    dao = InMemoryFeatureConfigDao(cache_file=str(cache_file))

    override = FeatureOverride(
        feature_name="dummy",
        user_id="user_1",
        value="enabled",
    )

    try:
        configure_feature_for_user("dummy", override, dao)
    except ValueError as exc:
        assert str(exc) == "Feature not found"
    else:
        assert False, "Expected ValueError when feature is missing"


def test_configure_feature_for_user_sets_timestamp(tmp_path):
    cache_file = tmp_path / "features.json"
    dao = InMemoryFeatureConfigDao(cache_file=str(cache_file))

    feature = Feature(
        feature_name="dummy",
        value="enabled",
    )
    dao.create_feature(feature)

    override = FeatureOverride(
        feature_name="dummy",
        user_id="user_2",
        value="disabled",
    )

    created = configure_feature_for_user("dummy", override, dao)

    assert created.timestamp is not None
