from fastapi import APIRouter, Depends, status
from services.project import ProjectService
from schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from core.dependencies import get_current_active_user, get_admin_user
from models.user import User
from typing import List

router = APIRouter()

@router.post("/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_admin_user),
    project_service: ProjectService = Depends()
) -> ProjectResponse:
    """
    Create a new project (admin only)
    """
    return project_service.create_project(project_data, current_user)

@router.get("/projects", response_model=List[ProjectResponse])
def get_projects(
    current_user: User = Depends(get_current_active_user),
    project_service: ProjectService = Depends()
) -> List[ProjectResponse]:
    """
    Get all projects (for all users)
    """
    return project_service.get_projects()

@router.get("/projects/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    current_user: User = Depends(get_current_active_user),
    project_service: ProjectService = Depends()
) -> ProjectResponse:
    """
    Get a project by ID
    """
    return project_service.get_project_by_id(project_id)

@router.put("/projects/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    current_user: User = Depends(get_current_active_user),
    project_service: ProjectService = Depends()
) -> ProjectResponse:
    """
    Update a project (admin or project owner)
    """
    return project_service.update_project(project_id, project_data, current_user)

@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    current_user: User = Depends(get_admin_user),
    project_service: ProjectService = Depends()
) -> None:
    """
    Delete a project (admin only)
    """
    project_service.delete_project(project_id, current_user)

