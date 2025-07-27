from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(min_length=8)
    tenant_id: UUID | None = None  # default to first tenant if not provided


class UserRead(UserBase):
    id: UUID
    tenant_id: UUID
    is_active: bool

    class Config:
        from_attributes = True
