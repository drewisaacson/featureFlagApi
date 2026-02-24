from abc import ABC, abstractmethod
from typing import Optional
from ..items.feature import Feature
from ..items.featureOverride import FeatureOverride


class FeatureConfigDao(ABC):
    """Abstract Data Access Object for feature configurations."""

    @abstractmethod
    def create_feature(self, feature: Feature) -> Feature:
        """Create or update a global feature flag."""
        pass

    @abstractmethod
    def get_feature(self, feature_name: str) -> Optional[Feature]:
        """Get a feature by name."""
        pass

    @abstractmethod
    def create_override(
        self, feature_name: str, override: FeatureOverride
    ) -> FeatureOverride:
        """Create a user-specific override."""
        pass

    @abstractmethod
    def get_override(
        self, feature_name: str, user_id: str
    ) -> Optional[FeatureOverride]:
        """Get an override for a specific user."""
        pass

    @abstractmethod
    def delete_override(
        self, feature_name: str, user_id: str
    ) -> Optional[FeatureOverride]:
        """Delete a user-specific override."""
        pass
