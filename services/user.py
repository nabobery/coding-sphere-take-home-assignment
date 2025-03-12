from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from core.db import get_session
from models.user import User
from schemas.user import UserResponse
from typing import List

class UserService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_users(self) -> List[UserResponse]:
        users = self.session.exec(select(User)).all()
        return [
            UserResponse(
                id=user.id,
                username=user.username,
                email=user.email,
                full_name=user.full_name,
                role=user.role,
                is_active=user.is_active,
                created_at=user.created_at,
            )
            for user in users
        ]

    def get_user_by_id(self, user_id: int) -> UserResponse:
        user = self.session.exec(select(User).where(User.id == user_id)).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found",
            )
        
        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at,
        )
