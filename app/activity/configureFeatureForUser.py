from datetime import datetime

from ..db.featureConfigDao import FeatureConfigDao
from ..items.featureOverride import FeatureOverride


def configure_feature_for_user(
    feature_name: str,
    override: FeatureOverride,
    dao: FeatureConfigDao,
) -> FeatureOverride:
    """
    Configure a feature flag override for a specific user.

    Args:
        feature_name: The name of the feature to override
        override: FeatureOverride object containing user_id, value, and
                  optional justification and timestamp
        dao: FeatureConfigDao instance for persisting the override

    Returns:
        The created FeatureOverride object with timestamp set

    Raises:
        ValueError: If the feature does not exist
    """
    if dao.get_feature(feature_name) is None:
        raise ValueError("Feature not found")
    if override.timestamp is None:
        # Set timestamp to now if not provided
        override = override.model_copy(
            update={"timestamp": datetime.now()}
        )
    return dao.create_override(feature_name, override)
