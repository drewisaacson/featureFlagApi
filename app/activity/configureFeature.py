from datetime import datetime

from ..items.feature import Feature
from ..db.featureConfigDao import FeatureConfigDao


def configure_feature(feature: Feature, dao: FeatureConfigDao) -> Feature:
    """
    Configure a feature flag in the system.

    Args:
        feature: Feature object containing feature_name, value,
                 feature_description, and timestamp
        dao: FeatureConfigDao instance for persisting the feature

    Returns:
        The configured Feature object
    """
    if feature.timestamp is None:
        feature = feature.model_copy(
            update={"timestamp": datetime.now()}
        )
    return dao.create_feature(feature)
