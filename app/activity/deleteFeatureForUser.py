from ..db.featureConfigDao import FeatureConfigDao
from ..items.featureOverride import FeatureOverride


def delete_feature_for_user(
    feature_name: str,
    user_id: str,
    dao: FeatureConfigDao,
) -> FeatureOverride:
    """
    Delete a user-specific feature override.

    Args:
        feature_name: The name of the feature
        user_id: The user ID whose override will be deleted
        dao: FeatureConfigDao instance for deleting the override

    Returns:
        The deleted FeatureOverride object

    Raises:
        ValueError: If the feature or override is not found
    """
    if dao.get_feature(feature_name) is None:
        raise ValueError(f"Feature {feature_name} not found")

    deleted = dao.delete_override(feature_name, user_id)
    if deleted is None:
        raise ValueError(
            f"Override for feature {feature_name} and user {user_id} not found"
        )
    return deleted
