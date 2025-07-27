"""Custom FastAPI-Users UserManager with tenant context."""
from uuid import UUID

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin, exceptions, models
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.core.database import get_db
from app.models.models import User

SECRET = "change_me"  # overridden by settings


async def get_user_db(session: AsyncSession = Depends(get_db)):
    yield SQLAlchemyUserDatabase(session, User)


class UserManager(IntegerIDMixin, BaseUserManager[User, UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Request | None = None):
        # Could send email or logging
        pass

    async def validate_password(self, password: str, user: User | models.UP):  # type: ignore[override]
        if len(password) < 8:
            raise exceptions.InvalidPasswordException(reason="Password should be at least 8 characters")
        return await super().validate_password(password, user)


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)
