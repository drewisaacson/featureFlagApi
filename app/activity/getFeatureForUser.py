from ..db.featureConfigDao import FeatureConfigDao
from ..items.featureOverride import FeatureOverride


def get_feature_for_user(
    feature_name: str,
    user_id: str,
    dao: FeatureConfigDao,
) -> FeatureOverride:
    """
    Retrieve a feature override for a specific user.

    Args:
        feature_name: The name of the feature
        user_id: The user ID
        dao: FeatureConfigDao instance for accessing the override

    Returns:
        The FeatureOverride object

    Raises:
        ValueError: If the feature is not found
    """
    override = dao.get_override(feature_name, user_id)
    if override is None:
        # check if the feature exists at all
        feat = dao.get_feature(feature_name)
        if feat is None:
            raise ValueError(f"Feature {feature_name} not found")
        # we use the feature's default value instead
        override = FeatureOverride(
            feature_name=feature_name,
            user_id=user_id,
            value=feat.value,
        )

    return override
