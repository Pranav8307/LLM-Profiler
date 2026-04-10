from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.profile import ProfileCreate, ProfileUpdate, ProfileResponse, ProfileListResponse
from app.services import profile as profile_service

router = APIRouter()


@router.post(
    "/",
    response_model=ProfileResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new LLM profile",
)
def create_profile(data: ProfileCreate, db: Session = Depends(get_db)):
    return profile_service.create_profile(db, data)


@router.get(
    "/",
    response_model=ProfileListResponse,
    summary="List all profiles",
)
def list_profiles(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    active_only: bool = Query(False),
    db: Session = Depends(get_db),
):
    total, items = profile_service.list_profiles(db, skip=skip, limit=limit, active_only=active_only)
    return ProfileListResponse(total=total, items=items)


@router.get(
    "/{profile_id}",
    response_model=ProfileResponse,
    summary="Get a single profile by ID",
)
def get_profile(profile_id: UUID, db: Session = Depends(get_db)):
    return profile_service.get_profile(db, profile_id)


@router.patch(
    "/{profile_id}",
    response_model=ProfileResponse,
    summary="Partially update a profile",
)
def update_profile(profile_id: UUID, data: ProfileUpdate, db: Session = Depends(get_db)):
    return profile_service.update_profile(db, profile_id, data)


@router.delete(
    "/{profile_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a profile",
)
def delete_profile(profile_id: UUID, db: Session = Depends(get_db)):
    profile_service.delete_profile(db, profile_id)