"""Pydantic request and response schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, HttpUrl


class HealthResponse(BaseModel):
    """Health check response."""

    status: str


class SiteCreate(BaseModel):
    """Request to add a monitored site."""

    url: HttpUrl


class SiteResponse(BaseModel):
    """A monitored site."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    url: str
    hostname: str
    verified: bool
    check_interval_s: int
    scan_interval_h: int
    created_at: datetime
