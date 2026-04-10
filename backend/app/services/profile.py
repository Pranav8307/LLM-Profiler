from uuid import UUID
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.models.profile import Profile
from app.schemas.profile import ProfileCreate, ProfileUpdate


def get_profile(db: Session, profile_id: UUID) -> Profile:
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Profile {profile_id} not found",
        )
    return profile


def get_profile_by_name(db: Session, name: str) -> Optional[Profile]:
    return db.query(Profile).filter(Profile.name == name).first()


def list_profiles(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    active_only: bool = False,
) -> tuple[int, list[Profile]]:
    query = db.query(Profile)
    if active_only:
        query = query.filter(Profile.is_active == True)  # noqa: E712
    total = query.count()
    items = query.order_by(Profile.created_at.desc()).offset(skip).limit(limit).all()
    return total, items


def create_profile(db: Session, data: ProfileCreate) -> Profile:
    profile = Profile(**data.model_dump())
    db.add(profile)
    try:
        db.commit()
        db.refresh(profile)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A profile named '{data.name}' already exists",
        )
    return profile


def update_profile(db: Session, profile_id: UUID, data: ProfileUpdate) -> Profile:
    profile = get_profile(db, profile_id)
    updates = data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(profile, field, value)
    db.commit()
    db.refresh(profile)
    return profile


def delete_profile(db: Session, profile_id: UUID) -> None:
    profile = get_profile(db, profile_id)
    db.delete(profile)
    db.commit()