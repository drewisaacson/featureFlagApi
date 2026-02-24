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
        ValueError: If the override is not found
    """
    override = dao.get_override(feature_name, user_id)
    if override is None:
        raise ValueError("Override not found")
    return override
