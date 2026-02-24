# app/db/inMemoryFeatureConfigDao.py
import json
from typing import Optional, Dict
from .featureConfigDao import FeatureConfigDao
from ..items.feature import Feature
from ..items.featureOverride import FeatureOverride


class InMemoryFeatureConfigDao(FeatureConfigDao):
    def __init__(self, cache_file: str = "/tmp/features.json"):
        self.features: Dict[str, Feature] = {}
        self.overrides: Dict[str, Dict[str, FeatureOverride]] = {}
        self.cache_file = cache_file
        self.last_cache_time = None
        self._load_from_file()

    def create_feature(self, feature: Feature) -> Feature:
        self.features[feature.feature_name] = feature
        self._save_to_file()
        return feature

    def get_feature(self, feature_name: str) -> Optional[Feature]:
        return self.features.get(feature_name)

    def create_override(
        self,
        feature_name: str,
        override: FeatureOverride,
    ) -> FeatureOverride:
        if feature_name not in self.overrides:
            self.overrides[feature_name] = {}
        self.overrides[feature_name][override.user_id] = override
        self._save_to_file()
        return override

    def get_override(
        self,
        feature_name: str,
        user_id: str,
    ) -> Optional[FeatureOverride]:
        return self.overrides.get(feature_name, {}).get(user_id)

    def delete_override(
        self,
        feature_name: str,
        user_id: str,
    ) -> Optional[FeatureOverride]:
        override = self.overrides.get(feature_name, {}).pop(user_id, None)
        if override:
            self._save_to_file()
        return override

    def _save_to_file(self):
        """Persist to file for durability"""
        try:
            data = {
                "features": {
                    k: v.model_dump(mode="json")
                    for k, v in self.features.items()
                },
                "overrides": {
                    k: {u: o.model_dump(mode="json") for u, o in v.items()}
                    for k, v in self.overrides.items()
                },
            }
            with open(self.cache_file, "w") as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error saving to file: {e}")

    def _load_from_file(self):
        """Load from persistent file on startup"""
        try:
            with open(self.cache_file, "r") as f:
                data = json.load(f)
                self.features = {
                    k: Feature(**v)
                    for k, v in data.get("features", {}).items()
                }
                self.overrides = {
                    k: {
                        u: FeatureOverride(**o)
                        for u, o in v.items()
                    }
                    for k, v in data.get("overrides", {}).items()
                }
        except FileNotFoundError:
            pass  # First startup
        except json.JSONDecodeError:
            pass  # Empty or corrupted cache file
