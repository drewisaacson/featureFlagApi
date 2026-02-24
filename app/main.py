from fastapi import FastAPI
import os
import logging

from .items.featureOverride import FeatureOverride
from .items.feature import Feature


app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8080))


@app.post("/feature")
def create_feature(feature: Feature):
    logger.info("Ingesting event for user %s", feature.feature_name)
    return {"status": "accepted"}


@app.post("/feature/{feature_name}")
def configure_feature_for_user(
    feature_name: str, config: FeatureOverride
):
    logger.info(
        "Configuring feature %s for user %s", feature_name, config.user_id
    )
    return {"status": "accepted", "feature": feature_name}


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
