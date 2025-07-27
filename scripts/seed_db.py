"""Seed database with initial tenant, roles, users, and sample dossier.
Run with:  python scripts/seed_db.py
Make sure Docker Compose services are running.
"""
import asyncio
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import AsyncSessionLocal, engine, Base
from app.models.models import Tenant, Role, User, Dossier, DossierStatusEnum
from app.core.security import get_password_hash


async def seed():
    async with AsyncSessionLocal() as session:  # type: AsyncSession
        # Ensure tables exist (for local quick start)
        async with engine.begin() as conn:
            # Create all tables if they don't exist (dev/local)
            await conn.run_sync(Base.metadata.create_all)

        # Check if already seeded
        res = await session.execute(select(Tenant).where(Tenant.name == "LabTest"))
        if res.scalar_one_or_none():
            print("Database already seeded. Skipping.")
            return

        tenant = Tenant(name="LabTest")
        session.add(tenant)
        await session.flush()

        admin_role = Role(tenant_id=tenant.id, name="admin", description="Administrateur laboratoire")
        user_role = Role(tenant_id=tenant.id, name="user", description="Utilisateur standard")
        session.add_all([admin_role, user_role])
        await session.flush()

        admin_user = User(
            tenant_id=tenant.id,
            role_id=admin_role.id,
            email="admin@labtest.com",
            hashed_password=get_password_hash("admin123"),
            is_superuser=True,
        )
        basic_user = User(
            tenant_id=tenant.id,
            role_id=user_role.id,
            email="user@labtest.com",
            hashed_password=get_password_hash("user123"),
        )
        session.add_all([admin_user, basic_user])
        await session.flush()

        dossier = Dossier(
            tenant_id=tenant.id,
            reference="AMM-DEMO-001",
            name_fr="Médicament Démo",
            name_ar="دواء تجريبي",
            status=DossierStatusEnum.draft,
            created_by=admin_user.id,
            progression_pct=10,
        )
        session.add(dossier)

        await session.commit()
        print("✔ Seed completed. Tenant LabTest with admin/user created.")


if __name__ == "__main__":
    asyncio.run(seed())
