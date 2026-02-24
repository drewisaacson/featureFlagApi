import pytest
from datetime import datetime
from pydantic import ValidationError

from app.items.featureOverride import FeatureOverride


class TestFeatureOverrideValidation:
    """Test cases for FeatureOverride model validation."""

    def test_featureoverride_valid_with_all_fields(self):
        """Test creating a FeatureOverride with all fields provided."""
        data = {
            "feature_name": "dark_mode",
            "user_id": "user_123",
            "value": "disabled",
            "justification": "User prefers light mode",
            "timestamp": datetime(2024, 1, 1, 12, 0, 0),
        }
        override = FeatureOverride(**data)
        assert override.feature_name == "dark_mode"
        assert override.user_id == "user_123"
        assert override.value == "disabled"
        assert override.justification == "User prefers light mode"

    def test_featureoverride_valid_without_optional_fields(self):
        """Test creating FeatureOverride with only required fields."""
        data = {
            "feature_name": "new_api",
            "user_id": "user_456",
            "value": "enabled",
            "timestamp": datetime.now(),
        }
        override = FeatureOverride(**data)
        assert override.feature_name == "new_api"
        assert override.user_id == "user_456"
        assert override.value == "enabled"
        assert override.justification is None

    def test_featureoverride_missing_feature_name(self):
        """Test that FeatureOverride requires feature_name."""
        data = {
            "user_id": "user_123",
            "value": "enabled",
            "timestamp": datetime.now(),
        }
        with pytest.raises(ValidationError) as exc_info:
            FeatureOverride(**data)
        assert "feature_name" in str(exc_info.value)

    def test_featureoverride_missing_user_id(self):
        """Test that FeatureOverride requires user_id."""
        data = {
            "feature_name": "test_feature",
            "value": "enabled",
            "timestamp": datetime.now(),
        }
        with pytest.raises(ValidationError) as exc_info:
            FeatureOverride(**data)
        assert "user_id" in str(exc_info.value)

    def test_featureoverride_missing_value(self):
        """Test that FeatureOverride requires value."""
        data = {
            "feature_name": "test_feature",
            "user_id": "user_123",
            "timestamp": datetime.now(),
        }
        with pytest.raises(ValidationError) as exc_info:
            FeatureOverride(**data)
        assert "value" in str(exc_info.value)

    def test_featureoverride_missing_timestamp(self):
        """Test that FeatureOverride requires timestamp."""
        data = {
            "feature_name": "test_feature",
            "user_id": "user_123",
            "value": "enabled",
        }
        with pytest.raises(ValidationError) as exc_info:
            FeatureOverride(**data)
        assert "timestamp" in str(exc_info.value)

    def test_featureoverride_empty_string_feature_name(self):
        """Test that empty string for feature_name is rejected."""
        data = {
            "feature_name": "",
            "user_id": "user_123",
            "value": "enabled",
            "timestamp": datetime.now(),
        }
        with pytest.raises(ValidationError) as exc_info:
            FeatureOverride(**data)
        assert "ensure this value has at least 1 character" in str(
            exc_info.value
        ) or "String should have at least 1 character" in str(exc_info.value)

    def test_featureoverride_empty_string_user_id(self):
        """Test that empty string for user_id is rejected."""
        data = {
            "feature_name": "test_feature",
            "user_id": "",
            "value": "enabled",
            "timestamp": datetime.now(),
        }
        with pytest.raises(ValidationError) as exc_info:
            FeatureOverride(**data)
        assert "ensure this value has at least 1 character" in str(
            exc_info.value
        ) or "String should have at least 1 character" in str(exc_info.value)

    def test_featureoverride_empty_string_value(self):
        """Test that empty string for value is rejected."""
        data = {
            "feature_name": "test_feature",
            "user_id": "user_123",
            "value": "",
            "timestamp": datetime.now(),
        }
        with pytest.raises(ValidationError) as exc_info:
            FeatureOverride(**data)
        assert "ensure this value has at least 1 character" in str(
            exc_info.value
        ) or "String should have at least 1 character" in str(exc_info.value)

    def test_featureoverride_empty_string_justification(self):
        """Test that empty string for justification is rejected."""
        data = {
            "feature_name": "test_feature",
            "user_id": "user_123",
            "value": "enabled",
            "justification": "",
            "timestamp": datetime.now(),
        }
        with pytest.raises(ValidationError) as exc_info:
            FeatureOverride(**data)
        assert "ensure this value has at least 1 character" in str(
            exc_info.value
        ) or "String should have at least 1 character" in str(exc_info.value)

    def test_featureoverride_invalid_timestamp_type(self):
        """Test that timestamp accepts string format."""
        data = {
            "feature_name": "test_feature",
            "user_id": "user_123",
            "value": "enabled",
            "timestamp": "2024-01-01",
        }
        override = FeatureOverride(**data)
        assert isinstance(override.timestamp, datetime)

    def test_featureoverride_with_iso_timestamp_string(self):
        """Test that ISO format timestamp strings are accepted."""
        data = {
            "feature_name": "test_feature",
            "user_id": "user_123",
            "value": "enabled",
            "timestamp": "2024-01-01T12:00:00",
        }
        override = FeatureOverride(**data)
        assert isinstance(override.timestamp, datetime)

    def test_featureoverride_with_special_characters_in_user_id(self):
        """Test that user_id can contain special characters."""
        data = {
            "feature_name": "test_feature",
            "user_id": "user-123@domain.com",
            "value": "enabled",
            "timestamp": datetime.now(),
        }
        override = FeatureOverride(**data)
        assert override.user_id == "user-123@domain.com"

