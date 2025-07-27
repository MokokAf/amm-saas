"""CRUD endpoints for dossiers with tenant ownership checks."""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from app.core.database import get_db
from app.models.models import Dossier, User
from app.schemas.dossier import (
    DossierCreate,
    DossierRead,
    DossierUpdate,
)
from app.routers.auth import current_active_user

router = APIRouter(prefix="/dossiers", tags=["Dossiers"])


@router.post("", response_model=DossierRead, status_code=status.HTTP_201_CREATED)
async def create_dossier(
    payload: DossierCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user),
):
    dossier = Dossier(
        tenant_id=user.tenant_id,
        reference=payload.reference,
        name_fr=payload.name_fr,
        name_ar=payload.name_ar,
        created_by=user.id,
    )
    db.add(dossier)
    await db.commit()
    await db.refresh(dossier)
    return dossier


@router.get("", response_model=list[DossierRead])
async def list_dossiers(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user),
):
    result = await db.execute(
        select(Dossier).where(Dossier.tenant_id == user.tenant_id)
    )
    return list(result.scalars().all())


@router.get("/{dossier_id}", response_model=DossierRead)
async def get_dossier(
    dossier_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user),
):
    dossier = await db.get(Dossier, dossier_id)
    if not dossier or dossier.tenant_id != user.tenant_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return dossier


@router.patch("/{dossier_id}", response_model=DossierRead)
async def update_dossier(
    dossier_id: UUID,
    payload: DossierUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user),
):
    dossier = await db.get(Dossier, dossier_id)
    if not dossier or dossier.tenant_id != user.tenant_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(dossier, field, value)
    await db.commit()
    await db.refresh(dossier)
    return dossier


@router.delete("/{dossier_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dossier(
    dossier_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user),
):
    dossier = await db.get(Dossier, dossier_id)
    if not dossier or dossier.tenant_id != user.tenant_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    await db.delete(dossier)
    await db.commit()
    return None
