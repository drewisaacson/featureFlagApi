from time import time
import logging
from typing import Optional, Dict

from .featureConfigDao import FeatureConfigDao
from .inMemoryFeatureConfigDao import InMemoryFeatureConfigDao
from ..items.feature import Feature
from ..items.featureOverride import FeatureOverride

logger = logging.getLogger(__name__)


class CachedFeatureConfigDao(FeatureConfigDao):
    """
    A caching wrapper around InMemoryFeatureConfigDao with TTL support.

    Caches feature and override lookups to improve performance.
    Cache entries automatically expire after the configured TTL.
    Write operations invalidate related cache entries.
    """

    def __init__(
        self,
        base_dao: InMemoryFeatureConfigDao,
        ttl_seconds: int = 300,
    ):
        self.base_dao = base_dao
        self.ttl = ttl_seconds
        self.feature_cache: Dict[str, Feature] = {}
        self.feature_cache_times: Dict[str, float] = {}
        self.override_cache: Dict[tuple, FeatureOverride] = {}
        self.override_cache_times: Dict[tuple, float] = {}
        logger.info(
            "Initialized CachedFeatureConfigDao with TTL=%d seconds",
            ttl_seconds,
        )

    def create_feature(self, feature: Feature) -> Feature:
        """Create feature and invalidate cache."""
        created = self.base_dao.create_feature(feature)
        self._invalidate_feature_cache(feature.feature_name)
        return created

    def get_feature(self, feature_name: str) -> Optional[Feature]:
        """Get feature from cache or base DAO."""
        if self._is_feature_cache_valid(feature_name):
            logger.debug(
                "Cache hit for feature: %s",
                feature_name,
            )
            return self.feature_cache.get(feature_name)

        logger.debug(
            "Cache miss for feature: %s - fetching from DAO",
            feature_name,
        )
        feature = self.base_dao.get_feature(feature_name)
        if feature:
            self.feature_cache[feature_name] = feature
            self.feature_cache_times[feature_name] = time()
            logger.debug(
                "Feature cached: %s",
                feature_name,
            )
        else:
            self._invalidate_feature_cache(feature_name)
        return feature

    def create_override(
        self,
        feature_name: str,
        override: FeatureOverride,
    ) -> FeatureOverride:
        """Create override and invalidate cache."""
        created = self.base_dao.create_override(feature_name, override)
        self._invalidate_override_cache(feature_name, override.user_id)
        return created

    def get_override(
        self,
        feature_name: str,
        user_id: str,
    ) -> Optional[FeatureOverride]:
        """Get override from cache or base DAO."""
        cache_key = (feature_name, user_id)
        if self._is_override_cache_valid(cache_key):
            logger.debug(
                "Cache hit for override: %s user %s",
                feature_name,
                user_id,
            )
            return self.override_cache.get(cache_key)

        logger.debug(
            "Cache miss for override: %s user %s - fetching from DAO",
            feature_name,
            user_id,
        )
        override = self.base_dao.get_override(feature_name, user_id)
        if override:
            self.override_cache[cache_key] = override
            self.override_cache_times[cache_key] = time()
            logger.debug(
                "Override cached: %s user %s",
                feature_name,
                user_id,
            )
        else:
            self._invalidate_override_cache(feature_name, user_id)
        return override

    def delete_override(
        self,
        feature_name: str,
        user_id: str,
    ) -> Optional[FeatureOverride]:
        """Delete override and invalidate cache."""
        deleted = self.base_dao.delete_override(feature_name, user_id)
        self._invalidate_override_cache(feature_name, user_id)
        return deleted

    def _is_feature_cache_valid(self, feature_name: str) -> bool:
        """Check if feature cache entry is still valid."""
        if feature_name not in self.feature_cache_times:
            return False
        return (time() - self.feature_cache_times[feature_name]) < self.ttl

    def _is_override_cache_valid(self, cache_key: tuple) -> bool:
        """Check if override cache entry is still valid."""
        if cache_key not in self.override_cache_times:
            return False
        return (
            time() - self.override_cache_times[cache_key]
        ) < self.ttl

    def _invalidate_feature_cache(self, feature_name: str) -> None:
        """Remove feature from cache."""
        self.feature_cache.pop(feature_name, None)
        self.feature_cache_times.pop(feature_name, None)

    def _invalidate_override_cache(
        self,
        feature_name: str,
        user_id: str,
    ) -> None:
        """Remove override from cache."""
        cache_key = (feature_name, user_id)
        self.override_cache.pop(cache_key, None)
        self.override_cache_times.pop(cache_key, None)
