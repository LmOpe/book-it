from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from api.v1.models.users import User
from api.v1.schemas.users import UserCreate
from api.utils.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token
    )

def create_user(db: Session, user_data: UserCreate):
    """Creates a new user with a hashed password"""

    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        hashed_password=hashed_password,
        role=user_data.role,
    )

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        ) from e

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        ) from e

def authenticate_user(db: Session, email: str, password: str):
    """Authenticates user credentials"""

    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def login_user(db: Session, email: str, password: str):
    """Logs in a user and returns an access token"""
    user = authenticate_user(db, email, password)
    if not user:
        return None
    token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token({"sub": user.email})
    return {"access_token": token, "refresh_token": refresh_token}
