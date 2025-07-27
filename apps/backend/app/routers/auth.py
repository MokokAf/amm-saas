"""Authentication routes using fastapi-users with JWT."""
from uuid import UUID

from fastapi import APIRouter
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)

from app.auth.manager import get_user_manager
from app.models.models import User
from app.core.config import get_settings

settings = get_settings()
router = APIRouter(prefix="/auth", tags=["Auth"])

# ── Auth backend (JWT) ───────────────────────────────────────────────

bearer_transport = BearerTransport(tokenUrl="/auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.JWT_SECRET, lifetime_seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)


auth_backend = AuthenticationBackend(name="jwt", transport=bearer_transport, get_strategy=get_jwt_strategy)


fastapi_users = FastAPIUsers[User, UUID](
    get_user_manager,
    [auth_backend],
)

# Register routes
router.include_router(fastapi_users.get_auth_router(auth_backend))
router.include_router(fastapi_users.get_register_router(UserRead="app.schemas.user:UserRead", UserCreate="app.schemas.user:UserCreate"))
router.include_router(fastapi_users.get_users_router(UserRead="app.schemas.user:UserRead", UserUpdate="app.schemas.user:UserCreate"))

# Current active user dependency for other routers
current_active_user = fastapi_users.current_user(active=True)
