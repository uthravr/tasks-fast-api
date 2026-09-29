from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.profile import Profile
from app.schemas.user import UserProfileResponse
from app.schemas.profile import ProfileCreate, ProfileUpdate, ProfileResponse
from app.utils.auth import get_current_user

router = APIRouter(prefix="/users", tags=["User Profiles"])

@router.post(
    "/profile",
    response_model=ProfileResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create User Profile",
    description="Adds profile details (phone number, address, date of birth, bio) for the authenticated user."
)
def create_profile(
    profile_in: ProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if a profile already exists for the user
    existing_profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile already exists for this user. Use PUT /users/profile to update."
        )

    # Create new profile record
    new_profile = Profile(
        user_id=current_user.id,
        phone_number=profile_in.phone_number,
        address=profile_in.address,
        date_of_birth=profile_in.date_of_birth,
        bio=profile_in.bio
    )
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return new_profile

@router.get(
    "/me",
    response_model=UserProfileResponse,
    summary="Get Own Profile",
    description="Retrieves the authenticated user's account details and profile information."
)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user

@router.get(
    "",
    response_model=List[UserProfileResponse],
    summary="List Registered Users",
    description="Retrieves a list of all registered users and their profiles."
)
def list_users(
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.put(
    "/profile",
    response_model=ProfileResponse,
    summary="Update User Profile",
    description="Updates profile details for the authenticated user. Only provided fields are updated."
)
def update_profile(
    profile_in: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found. Please create a profile first using POST /users/profile."
        )

    update_data = profile_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)
    return profile

@router.delete(
    "/profile",
    summary="Delete User Profile",
    description="Deletes the authenticated user's profile while retaining their user account."
)
def delete_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found. Nothing to delete."
        )

    db.delete(profile)
    db.commit()
    return {"message": "User profile deleted successfully."}
