from fastapi import FastAPI, HTTPException
import logging
import os

from .activity.configureFeature import (
    configure_feature as configure_feature_activity,
)
from .activity.configureFeatureForUser import (
    configure_feature_for_user as configure_feature_for_user_activity,
)
from .activity.getFeature import get_feature as get_feature_activity
from .activity.getFeatureForUser import (
    get_feature_for_user as get_feature_for_user_activity,
)
from .db.cachedFeatureConfigDao import CachedFeatureConfigDao
from .db.inMemoryFeatureConfigDao import InMemoryFeatureConfigDao
from .items.feature import Feature
from .items.featureOverride import FeatureOverride


app = FastAPI()
base_dao = InMemoryFeatureConfigDao()
dao = CachedFeatureConfigDao(base_dao, ttl_seconds=300)

log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8080))


@app.post("/feature")
def configure_feature(feature: Feature):
    logger.info("Configuring feature %s", feature.feature_name)
    configuredFeat = configure_feature_activity(feature, dao)
    return {"status": "accepted", "feature": configuredFeat.model_dump()}


@app.post("/feature/{feature_name}")
def configure_feature_for_user(
    feature_name: str, config: FeatureOverride
):
    logger.info(
        "Configuring feature %s for user %s", feature_name, config.user_id
    )
    if dao.get_feature(feature_name) is None:
        raise HTTPException(
            status_code=404,
            detail="Feature not found",
        )
    configuredFeat = configure_feature_for_user_activity(
        feature_name, config, dao)
    return {
        "status": "accepted",
        "feature": feature_name,
        "override": configuredFeat.model_dump(),
    }


@app.get("/feature/{feature_name}")
def get_feature(feature_name: str):
    logger.info("Retrieving feature %s", feature_name)
    try:
        feature = get_feature_activity(feature_name, dao)
        return {"status": "ok", "feature": feature.model_dump()}
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Feature not found",
        )


@app.get("/feature/{feature_name}/user/{user_id}")
def get_feature_for_user(feature_name: str, user_id: str):
    logger.info(
        "Retrieving feature %s for user %s", feature_name, user_id
    )
    try:
        override = get_feature_for_user_activity(
            feature_name, user_id, dao
        )
        return {"status": "ok", "override": override.model_dump()}
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Override not found",
        )


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        log_level=log_level.lower(),
    )
