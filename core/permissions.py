from enum import Enum, auto
from typing import List, Optional
from fastapi import Depends, HTTPException, status
from models.user import User

class Permission(Enum):
    READ = auto()
    CREATE = auto()
    UPDATE = auto()
    DELETE = auto()

class RolePermission:
    def __init__(self, role: str, permissions: List[Permission]):
        self.role = role
        self.permissions = permissions

# Define permissions for roles
ROLE_PERMISSIONS = {
    "admin": RolePermission("admin", [Permission.READ, Permission.CREATE, Permission.UPDATE, Permission.DELETE]),
    "user": RolePermission("user", [Permission.READ]),
}

def check_permissions(user: User, required_permission: Permission) -> bool:
    """Check if a user has the required permission."""
    if user.role not in ROLE_PERMISSIONS:
        return False
    
    role_permission = ROLE_PERMISSIONS[user.role]
    return required_permission in role_permission.permissions