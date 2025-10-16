from fastapi import HTTPException
from sqlalchemy.orm import Session
from core.services.projects_service import get_role

def require_project_manager(db: Session, project_id: int, person_id: int):
    """
    فقط مدیر پروژه (MANAGER) اجازه انجام عملیات دارد.
    """
    role = get_role(db, project_id, person_id)
    if role != "MANAGER":
        raise HTTPException(status_code=403, detail="Only MANAGER can perform this action")
    return role

def require_project_member(db: Session, project_id: int, person_id: int):
    """
    هر کسی که عضو پروژه باشد (نقش غیر None)، اجازه دارد.
    """
    role = get_role(db, project_id, person_id)
    if role is None:
        raise HTTPException(status_code=403, detail="You must be a project member to perform this action")
    return role
