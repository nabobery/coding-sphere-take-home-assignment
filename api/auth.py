from fastapi import APIRouter, Depends, status
from services.auth import AuthService
from schemas.user import UserCreate, UserLogin, UserResponse, Token

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserCreate, 
    auth_service: AuthService = Depends()
) -> UserResponse:
    user = auth_service.register_user(user_data)
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        is_active=user.is_active,
        created_at=user.created_at,
    )

@router.post("/login", response_model=Token)
def login(
    user_data: UserLogin,
    auth_service: AuthService = Depends()
) -> Token:
    return auth_service.authenticate_user(user_data)
