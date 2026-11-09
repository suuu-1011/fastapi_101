import os
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from .database import get_db
from . import models, schemas
from .security import hash_password, verify_password, create_token, hash_token, decode_token

from .dependencies import get_current_user
import jwt 
import hmac

load_dotenv()

router = APIRouter(prefix="/auth", tags=["Authentication"])

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15")
)

REFRESH_TOKEN_EXPIRE_DAYS = int(
    os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7")
)


# REGISTER
@router.post("/register", status_code=201)
def register(user_data: schemas.AuthRegister, db: Session = Depends(get_db)):

    existing_user = db.query(models.User).filter(
        models.User.email == user_data.email.lower()
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = models.User(
        name=user_data.name,
        email=user_data.email.lower(),
        phone=user_data.phone,
        password_hash=hash_password(user_data.password),
        role="student",
        status="active"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Student registered successfully",
        "user_id": new_user.id
    }


# LOGIN
@router.post("/login", response_model=schemas.TokenResponse)
def login(user_data: schemas.AuthLogin, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(
        models.User.email == user_data.email.lower()
    ).first()

    if not user or not user.password_hash:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if user.status != "active":
        raise HTTPException(
            status_code=403,
            detail="Account is inactive"
        )

    now = datetime.now(timezone.utc)

    refresh_expiry = now + timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS
    )

    # Create session first to obtain its database ID
    new_session = models.AuthSession(
        user_id=user.id,
        refresh_token_hash="pending",
        expires_at=refresh_expiry
    )

    db.add(new_session)
    db.flush()

    # Generate access token
    access_token = create_token(
        {
            "sub": str(user.id),
            "role": user.role,
            "sid": new_session.id,
            "type": "access"
        },
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    # Generate refresh token
    refresh_token = create_token(
        {
            "sub": str(user.id),
            "sid": new_session.id,
            "type": "refresh"
        },
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

    # Store only the hash of the refresh token
    new_session.refresh_token_hash = hash_token(refresh_token)

    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
#REGISTRATION AND LOGIN

@router.post("/refresh", response_model=schemas.TokenResponse)
def refresh_token(
    token_data: schemas.RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    try:
        payload = decode_token(token_data.refresh_token)
    except jwt.InvalidTokenError:
        raise HTTPException(401, detail="Invalid or expired refresh token")

    if payload.get("type") != "refresh":
        raise HTTPException(401, detail="Refresh token required")

    user_id = payload.get("sub")
    session_id = payload.get("sid")

    if not user_id or not session_id:
        raise HTTPException(401, detail="Invalid token data")

    auth_session = db.query(models.AuthSession).filter(
        models.AuthSession.id == int(session_id),
        models.AuthSession.user_id == int(user_id)
    ).first()

    if not auth_session:
        raise HTTPException(401, detail="Session not found")

    if auth_session.revoked_at is not None:
        raise HTTPException(401, detail="Session has been revoked")

    now = datetime.now(timezone.utc)

    if auth_session.expires_at <= now:
        raise HTTPException(401, detail="Session has expired")

    if not hmac.compare_digest(
        auth_session.refresh_token_hash,
        hash_token(token_data.refresh_token)
    ):
        raise HTTPException(401, detail="Refresh token is no longer valid")

    user = db.query(models.User).filter(
        models.User.id == int(user_id)
    ).first()

    if not user or user.status != "active":
        raise HTTPException(401, detail="User not found or inactive")

    new_refresh_expiry = now + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    new_access_token = create_token(
        {
            "sub": str(user.id),
            "role": user.role,
            "sid": auth_session.id,
            "type": "access"
        },
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    new_refresh_token = create_token(
        {
            "sub": str(user.id),
            "sid": auth_session.id,
            "type": "refresh"
        },
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

    auth_session.refresh_token_hash = hash_token(new_refresh_token)
    auth_session.expires_at = new_refresh_expiry

    db.commit()

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }

@router.post("/logout")
def logout(
    token_data: schemas.RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    try:
        payload = decode_token(token_data.refresh_token)
    except jwt.InvalidTokenError:
        raise HTTPException(401, detail="Invalid or expired refresh token")

    if payload.get("type") != "refresh":
        raise HTTPException(401, detail="Refresh token required")

    user_id = payload.get("sub")
    session_id = payload.get("sid")

    if not user_id or not session_id:
        raise HTTPException(401, detail="Invalid token data")

    auth_session = db.query(models.AuthSession).filter(
        models.AuthSession.id == int(session_id),
        models.AuthSession.user_id == int(user_id)
    ).first()

    if not auth_session:
        raise HTTPException(401, detail="Session not found")

    if auth_session.revoked_at is not None:
        raise HTTPException(401, detail="Session already revoked")

    if auth_session.expires_at <= datetime.now(timezone.utc):
        raise HTTPException(401, detail="Session has expired")

    if not hmac.compare_digest(
        auth_session.refresh_token_hash,
        hash_token(token_data.refresh_token)
    ):
        raise HTTPException(401, detail="Invalid refresh token")

    auth_session.revoked_at = datetime.now(timezone.utc)
    db.commit()

    return {"message": "Logged out successfully"}

@router.get("/me", response_model=schemas.AuthUserResponse)
def get_my_profile(
    current_user: models.User = Depends(get_current_user)
):
    return current_user

