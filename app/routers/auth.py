from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserRegister, UserLogin, UserResponse, LoginResponse
from app.utils.security import hash_password, verify_password
from app.utils.auth import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="User Registration",
    description="Registers a new user with name, email, and password. Checks for duplicate email and hashes password securely."
)
def register_user(user_in: UserRegister, db: Session = Depends(get_db)):
    # Check if a user with this email already exists
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered. Please use another email or log in."
        )

    # Hash the password securely
    hashed_pwd = hash_password(user_in.password)

    # Create new user record
    new_user = User(
        name=user_in.name,
        email=user_in.email,
        hashed_password=hashed_pwd
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post(
    "/login",
    response_model=LoginResponse,
    summary="User Login",
    description="Authenticates user by email and password, returning a JWT Bearer access token."
)
def login_user(credentials: UserLogin, db: Session = Depends(get_db)):
    # Find user by email
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    # Verify password against stored hash
    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    # Generate JWT token
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email}
    )

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )
