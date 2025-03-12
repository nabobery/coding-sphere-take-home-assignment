from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from core.db import get_session
from models.project import Project
from models.user import User
from schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from typing import List
from datetime import datetime

class ProjectService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create_project(self, project_data: ProjectCreate, current_user: User) -> ProjectResponse:
        project = Project(
            name=project_data.name,
            description=project_data.description,
            owner_id=current_user.id,
        )
        
        self.session.add(project)
        self.session.commit()
        self.session.refresh(project)
        
        return ProjectResponse(
            id=project.id,
            name=project.name,
            description=project.description,
            owner_id=project.owner_id,
            created_at=project.created_at,
            updated_at=project.updated_at,
        )

    def get_projects(self) -> List[ProjectResponse]:
        projects = self.session.exec(select(Project)).all()
        return [
            ProjectResponse(
                id=project.id,
                name=project.name,
                description=project.description,
                owner_id=project.owner_id,
                created_at=project.created_at,
                updated_at=project.updated_at,
            )
            for project in projects
        ]

    def get_project_by_id(self, project_id: int) -> ProjectResponse:
        project = self.session.exec(select(Project).where(Project.id == project_id)).first()
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with ID {project_id} not found",
            )
        
        return ProjectResponse(
            id=project.id,
            name=project.name,
            description=project.description,
            owner_id=project.owner_id,
            created_at=project.created_at,
            updated_at=project.updated_at,
        )

    def update_project(self, project_id: int, project_data: ProjectUpdate, current_user: User) -> ProjectResponse:
        project = self.session.exec(select(Project).where(Project.id == project_id)).first()
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with ID {project_id} not found",
            )
        
        # Check if user is admin or is the owner of the project
        if current_user.role != "admin" and project.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to update this project",
            )
        
        # Update project fields
        if project_data.name is not None:
            project.name = project_data.name
        if project_data.description is not None:
            project.description = project_data.description
        
        project.updated_at = datetime.utcnow()
        
        self.session.add(project)
        self.session.commit()
        self.session.refresh(project)
        
        return ProjectResponse(
            id=project.id,
            name=project.name,
            description=project.description,
            owner_id=project.owner_id,
            created_at=project.created_at,
            updated_at=project.updated_at,
        )

    def delete_project(self, project_id: int, current_user: User) -> None:
        project = self.session.exec(select(Project).where(Project.id == project_id)).first()
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with ID {project_id} not found",
            )
        
        # Check if user is admin or is the owner of the project
        if current_user.role != "admin" and project.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to delete this project",
            )
        
        self.session.delete(project)
        self.session.commit()
