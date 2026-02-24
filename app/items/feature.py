from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class Feature(BaseModel):
    feature_name: str = Field(
        ..., min_length=1, description="The name of the feature flag"
    )
    value: str = Field(
        ..., min_length=1,
        description="The feature flag value or status"
    )
    feature_description: Optional[str] = Field(
        default=None, min_length=1,
        description="Optional description of the feature"
    )
    timestamp: Optional[datetime] = Field(
        default=None,
        description="The timestamp when this configuration was created"
    )
