from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.core.config import settings
from api.v1.schemas.users import (
    UserCreate,
    UserLogin,
    UserResponse,
    LoginResponse
)
from api.v1.services.users import create_user, login_user
from api.db.db import get_db
from api.utils.response_model import success_response, error_response

auth = APIRouter(prefix="/auth", tags=["Authentication"])

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


@auth.post("/signup", response_model=UserResponse)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        user = create_user(db, user_data)
        user_data = UserResponse(
            id=user.id,
            full_name=user.full_name,
            email=user.email,
            role=user.role,
            is_active=user.is_active,
        )
        return success_response(
            status_code=status.HTTP_201_CREATED,
            message="User created successfully",
            data=user_data,
        )
    except HTTPException as e:
        return error_response(
            status_code=e.status_code,
            message=e.detail,
        )
    except Exception as e:
        return error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="An unexpected error occurred",
            data={"error": str(e)},
        )


@auth.post("/login", response_model=LoginResponse)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    tokens = login_user(db, user_data.email, user_data.password)

    if not tokens:
        return error_response(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="Invalid credentials"
        )
    data = LoginResponse(**tokens)
    return success_response(
        status_code=status.HTTP_200_OK,
        message="Login successful",
        data=data
    )
