from datetime import datetime

from ..db.featureConfigDao import FeatureConfigDao
from ..items.featureOverride import FeatureOverride


def configure_feature_for_user(
    feature_name: str,
    override: FeatureOverride,
    dao: FeatureConfigDao,
) -> FeatureOverride:
    if override.timestamp is None:
        # Set timestamp to now if not provided
        override = override.model_copy(
            update={"timestamp": datetime.now()}
        )
    return dao.create_override(feature_name, override)
