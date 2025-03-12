from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from datetime import datetime


class ProjectBase(SQLModel):
    name: str
    description: Optional[str] = None

class Project(ProjectBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    owner: "User" = Relationship(back_populates="projects")
