from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class FeatureOverride(BaseModel):
    feature_name: str = Field(
        ..., min_length=1, description="The name of the feature flag"
    )
    user_id: str = Field(
        ..., min_length=1,
        description="The user ID for whom the override applies"
    )
    value: str = Field(
        ..., min_length=1, description="The feature flag value or status"
    )
    justification: Optional[str] = Field(
        default=None, min_length=1,
        description="Optional override justification"
    )
    timestamp: datetime = Field(
        description="The timestamp when this configuration was created"
    )
