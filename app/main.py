from fastapi import FastAPI, HTTPException
import logging
import os

from .activity.configureFeature import (
    configure_feature as configure_feature_activity,
)
from .activity.configureFeatureForUser import (
    configure_feature_for_user as configure_feature_for_user_activity,
)
from .db.inMemoryFeatureConfigDao import InMemoryFeatureConfigDao
from .items.feature import Feature
from .items.featureOverride import FeatureOverride


app = FastAPI()
dao = InMemoryFeatureConfigDao()

logging.basicConfig(level=logging.INFO)
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
    default = {
        "feature_name": feature_name,
    }

    return default


@app.get("/feature/{feature_name}/user/{user_id}")
def get_feature_for_user(feature_name: str, user_id: str):
    feature = {
        "feature_name": feature_name,
        "user_id": user_id,
        "enabled": True
    }

    return feature


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
