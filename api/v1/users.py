"""User API endpoints."""

from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from models.user import User
from schemas.user import UserCreate, UserResponse, UserLogin, Token, UserUpdate
from core.security import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    get_current_active_user,
)
from core.config import settings


router = APIRouter()


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register(user_data: UserCreate):
    """Register a new user."""
    # Check if user already exists
    existing_user = await User.find_one(User.email == user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # Create new user
    user = User(
        email=user_data.email,
        phone=user_data.phone,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        hashed_password=User.get_password_hash(user_data.password),
    )
    await user.insert()

    return UserResponse(
        id=str(user.id),
        email=user.email,
        phone=user.phone,
        first_name=user.first_name,
        last_name=user.last_name,
        is_active=user.is_active,
        is_staff=user.is_staff,
        is_superuser=user.is_superuser,
        date_joined=user.date_joined,
        last_login=user.last_login,
    )


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    """Login user and return tokens."""
    user = await User.find_one(User.email == credentials.email)

    if not user or not user.verify_password(credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    # Create tokens
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    # Update last login
    user.last_login = datetime.utcnow()
    await user.save()

    return Token(access_token=access_token, refresh_token=refresh_token)


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """Get current user information."""
    return UserResponse(
        id=str(current_user.id),
        email=current_user.email,
        phone=current_user.phone,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        is_active=current_user.is_active,
        is_staff=current_user.is_staff,
        is_superuser=current_user.is_superuser,
        date_joined=current_user.date_joined,
        last_login=current_user.last_login,
    )


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate, current_user: User = Depends(get_current_active_user)
):
    """Update current user information."""
    if user_update.phone is not None:
        current_user.phone = user_update.phone
    if user_update.first_name is not None:
        current_user.first_name = user_update.first_name
    if user_update.last_name is not None:
        current_user.last_name = user_update.last_name

    await current_user.save()

    return UserResponse(
        id=str(current_user.id),
        email=current_user.email,
        phone=current_user.phone,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        is_active=current_user.is_active,
        is_staff=current_user.is_staff,
        is_superuser=current_user.is_superuser,
        date_joined=current_user.date_joined,
        last_login=current_user.last_login,
    )


# Made with Bob
