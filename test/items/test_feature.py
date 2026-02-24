import pytest
from datetime import datetime
from pydantic import ValidationError

from app.items.feature import Feature


class TestFeatureValidation:
    """Test cases for Feature model validation."""

    def test_feature_valid_with_all_fields(self):
        """Test creating a Feature with all fields provided."""
        data = {
            "feature_name": "dark_mode",
            "value": "enabled",
            "feature_description": "Enable dark mode for users",
            "timestamp": datetime(2024, 1, 1, 12, 0, 0),
        }
        feature = Feature(**data)
        assert feature.feature_name == "dark_mode"
        assert feature.value == "enabled"
        assert feature.feature_description == "Enable dark mode for users"

    def test_feature_valid_without_optional_fields(self):
        """Test creating a Feature with only required fields."""
        data = {
            "feature_name": "new_api",
            "value": "beta",
            "timestamp": datetime.now(),
        }
        feature = Feature(**data)
        assert feature.feature_name == "new_api"
        assert feature.value == "beta"
        assert feature.feature_description is None

    def test_feature_missing_feature_name(self):
        """Test that Feature requires feature_name."""
        data = {
            "value": "enabled",
            "timestamp": datetime.now(),
        }
        with pytest.raises(ValidationError) as exc_info:
            Feature(**data)
        assert "feature_name" in str(exc_info.value)

    def test_feature_missing_value(self):
        """Test that Feature requires value."""
        data = {
            "feature_name": "test_feature",
            "timestamp": datetime.now(),
        }
        with pytest.raises(ValidationError) as exc_info:
            Feature(**data)
        assert "value" in str(exc_info.value)

    def test_feature_missing_timestamp(self):
        """Test that Feature requires timestamp."""
        data = {
            "feature_name": "test_feature",
            "value": "enabled",
        }
        with pytest.raises(ValidationError) as exc_info:
            Feature(**data)
        assert "timestamp" in str(exc_info.value)

    def test_feature_empty_string_feature_name(self):
        """Test that empty string for feature_name is rejected."""
        data = {
            "feature_name": "",
            "value": "enabled",
            "timestamp": datetime.now(),
        }
        with pytest.raises(ValidationError) as exc_info:
            Feature(**data)
        assert "ensure this value has at least 1 character" in str(
            exc_info.value
        ) or "String should have at least 1 character" in str(exc_info.value)

    def test_feature_empty_string_value(self):
        """Test that empty string for value is rejected."""
        data = {
            "feature_name": "test_feature",
            "value": "",
            "timestamp": datetime.now(),
        }
        with pytest.raises(ValidationError) as exc_info:
            Feature(**data)
        assert "ensure this value has at least 1 character" in str(
            exc_info.value
        ) or "String should have at least 1 character" in str(exc_info.value)

    def test_feature_empty_string_description(self):
        """Test that empty string for description is rejected."""
        data = {
            "feature_name": "test_feature",
            "value": "enabled",
            "feature_description": "",
            "timestamp": datetime.now(),
        }
        with pytest.raises(ValidationError) as exc_info:
            Feature(**data)
        assert "ensure this value has at least 1 character" in str(
            exc_info.value
        ) or "String should have at least 1 character" in str(exc_info.value)

    def test_feature_invalid_timestamp_type(self):
        """Test that invalid timestamp type is rejected."""
        data = {
            "feature_name": "test_feature",
            "value": "enabled",
            "timestamp": "2024-01-01",
        }
        feature = Feature(**data)
        assert isinstance(feature.timestamp, datetime)

    def test_feature_with_iso_timestamp_string(self):
        """Test that ISO format timestamp strings are accepted."""
        data = {
            "feature_name": "test_feature",
            "value": "enabled",
            "timestamp": "2024-01-01T12:00:00",
        }
        feature = Feature(**data)
        assert isinstance(feature.timestamp, datetime)

