from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from core.db import get_session
from models.user import User
from core.security import get_password_hash, verify_password, create_access_token
from schemas.user import UserCreate, UserLogin, UserResponse, Token
from typing import Optional
from datetime import timedelta
from config.config import settings

class AuthService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def register_user(self, user_data: UserCreate) -> User:
        # Check if username already exists
        user_exists = self.session.exec(
            select(User).where(User.username == user_data.username)
        ).first()
        
        if user_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered",
            )
        
        # Create new user
        hashed_password = get_password_hash(user_data.password)
        user = User(
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            role=user_data.role,
            hashed_password=hashed_password,
        )
        
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        
        return user

    def authenticate_user(self, user_data: UserLogin) -> Optional[Token]:
        user = self.session.exec(
            select(User).where(User.username == user_data.username)
        ).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not verify_password(user_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
        
        # Convert User model to UserResponse
        user_response = UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at,
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            user=user_response,
        )
