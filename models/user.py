from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from datetime import datetime
from enum import Enum as PyEnum

class UserRole(str, PyEnum):
    ADMIN = "admin"
    USER = "user"

class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    email: Optional[str] = Field(default=None, index=True, unique=True)
    full_name: Optional[str] = None
    role: UserRole = Field(default=UserRole.USER)
    is_active: bool = Field(default=True)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    projects: List["Project"] = Relationship(back_populates="owner")