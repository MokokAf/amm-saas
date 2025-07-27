from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class DossierBase(BaseModel):
    reference: str = Field(max_length=100)
    name_fr: str
    name_ar: str


class DossierCreate(DossierBase):
    pass


class DossierUpdate(BaseModel):
    status: str | None = None  # draft, submitted, approved, etc.
    progression_pct: int | None = Field(default=None, ge=0, le=100)


class DossierRead(DossierBase):
    id: UUID
    status: str
    progression_pct: int | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
