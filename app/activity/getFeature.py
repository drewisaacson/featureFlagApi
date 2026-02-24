from ..db.featureConfigDao import FeatureConfigDao
from ..items.feature import Feature


def get_feature(feature_name: str, dao: FeatureConfigDao) -> Feature:
    """
    Retrieve a feature flag by name.

    Args:
        feature_name: The name of the feature to retrieve
        dao: FeatureConfigDao instance for accessing the feature

    Returns:
        The Feature object

    Raises:
        ValueError: If the feature is not found
    """
    feature = dao.get_feature(feature_name)
    if feature is None:
        raise ValueError("Feature not found")
    return feature
