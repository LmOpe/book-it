from datetime import datetime, timedelta, UTC
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi import HTTPException, status
from api.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:

    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=settings.ACCESS_TOKEN_LIFETIME)):
    to_encode = data.copy()
    expire = datetime.now(UTC) + expires_delta
    to_encode.update({"exp": expire, "type": "access"})
    access_token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return access_token

def create_refresh_token(data: dict, expires_delta: timedelta = timedelta(days=settings.REFRESH_TOKEN_LIFETIME)):
    to_encode = data.copy()
    expire = datetime.now(UTC) + expires_delta
    to_encode.update({"exp": expire, "type": "refresh"})
    refresh_token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return refresh_token

def refresh_access_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
        user_email = payload.get("sub")

        if user_email is None:
            raise jwt.JWTError("Invalid refresh token")

        access_token = create_access_token({"sub": user_email})
        return access_token

    except jwt.ExpiredSignatureError as exc:
        raise jwt.ExpiredSignatureError("Refresh token has expired") from exc

    except jwt.JWTError as exc:
        raise ValueError("Invalid refresh token") from exc

def verify_token(token: str, expected_type: str):
    """Verifies any token, ensuring it matches the expected type and is not expired."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        exp = payload.get("exp")
        token_type = payload.get("type")

        if exp is None or token_type is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        if datetime.now(UTC).timestamp() > exp:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )

        # Ensure the correct token type (access or refresh)
        if token_type != expected_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token type, expected {expected_type}"
            )

        return payload

    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        ) from exc

def verify_access_token(token: str):
    """Verifies the access token and checks expiration."""
    return verify_token(token, expected_type="access")

def verify_refresh_token(token: str):
    """Verifies the refresh token and checks expiration."""
    return verify_token(token, expected_type="refresh")
