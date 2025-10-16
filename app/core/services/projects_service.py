from typing import List, Optional
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import select
from db.schemas.ProjectDocuments import ProjectDocumentUpdate
from db.models.projects import projects
from db.models.ProjectMembers import ProjectMembers
from db.models.ProjectDocuments import ProjectDocuments
from db.schemas.projects import ProjectCreate, ProjectUpdate
from fastapi import HTTPException

# ---- خواندن پروژه تکی
def get_project_by_id(db: Session, project_id: int) -> Optional[projects]:
    return db.execute(
        select(projects).where(projects.ProjectID == project_id)
    ).scalar_one_or_none()

# ---- فهرست پروژه‌ها برای یک شخص (فقط پروژه‌هایی که عضو آنهاست)
def list_projects_for_person(
    db: Session,
    person_id: int,
    title: str = "",
    project_status: str = "",
) -> List[projects]:
    stmt = (
        select(projects)
        .join(ProjectMembers, ProjectMembers.ProjectID == projects.ProjectID)
        .where(
            ProjectMembers.PersonID == person_id,
            projects.DeleteFlag == "NO",
        )
    )
    if title:
        stmt = stmt.where(projects.title.ilike(f"%{title}%"))
    if project_status:
        stmt = stmt.where(projects.ProjectStatus == project_status)

    return list(db.execute(stmt).scalars().all())


# ---- اعضای پروژه
def get_members(db: Session, project_id: int) -> List[ProjectMembers]:
    stmt = select(ProjectMembers).where(ProjectMembers.ProjectID == project_id)
    return list(db.execute(stmt).scalars().all())

# --- اضافه کردن عضو به پروژه (فقط مدیر)
def add_member(db: Session, project_id: int, person_id: int, access_type: str, creator_id: int) -> ProjectMembers:
    new_member = ProjectMembers(
        ProjectID=project_id,
        PersonID=person_id,
        AccessType=access_type,
        ParticipationPercent=100,
        CreatorID=creator_id
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member

# --- حذف عضو از پروژه (فقط مدیر)
def remove_member(db: Session, project_id: int, person_id: int) -> bool:
    member = db.execute(
        select(ProjectMembers).where(
            ProjectMembers.ProjectID == project_id,
            ProjectMembers.PersonID == person_id
        )
    ).scalar_one_or_none()

    if not member:
        return False

    db.delete(member)
    db.commit()
    return True

# ---- مستندات پروژه
def get_documents(db: Session, project_id: int) -> List[ProjectDocuments]:
    stmt = select(ProjectDocuments).where(ProjectDocuments.ProjectID == project_id)
    return list(db.execute(stmt).scalars().all())

# --- اضافه کردن داکیومنت (هر عضو می‌تواند)
def add_document(db: Session, project_id: int, creator_id: int, file_name: str, file_content: bytes, description: Optional[str] = None, document_date: Optional[datetime] = None, doc_type_id: int = 1) -> ProjectDocuments:
    doc = ProjectDocuments(
        ProjectID=project_id,
        ProjectDocumentTypeID=doc_type_id,
        FileName=file_name,
        FileContent=file_content,
        CreatorID=creator_id,
        CreateDate=datetime.now(),
        DocumentDate=document_date or datetime.now(),
        description=description
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc

# --- حذف داکیومنت
def remove_document(db: Session, project_id: int, document_id: int, requester_id: int, requester_role: str) -> bool:
    doc = db.execute(
        select(ProjectDocuments).where(
            ProjectDocuments.ProjectID == project_id,
            ProjectDocuments.ProjectDocumentID == document_id
        )
    ).scalar_one_or_none()

    if not doc:
        return False

    # فقط مدیر یا سازنده داکیومنت اجازه دارد
    if requester_role != "MANAGER" and doc.CreatorID != requester_id:
        raise HTTPException(status_code=403, detail="Not allowed to delete this document")

    db.delete(doc)
    db.commit()
    return True

# --- ویرایش داکیومنت
def update_document(
    db: Session,
    document_id: int,
    requester_id: int,
    requester_role: str,
    updates: dict
) -> Optional[ProjectDocuments]:
    doc = db.execute(
        select(ProjectDocuments).where(
            ProjectDocuments.ProjectDocumentID == document_id
        )
    ).scalar_one_or_none()

    if not doc:
        return None

    if requester_role != "MANAGER" and doc.CreatorID != requester_id:
        raise HTTPException(status_code=403, detail="Not allowed to update this document")

    for field, value in updates.items():
        setattr(doc, field, value)

    db.commit()
    db.refresh(doc)
    return doc

# --- گرفتن داکیومنت با id یا خطای 404
def get_document_or_404(db: Session, document_id: int) -> ProjectDocuments:
    doc = db.execute(
        select(ProjectDocuments).where(ProjectDocuments.ProjectDocumentID == document_id)
    ).scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

# ---- نقش فرد در پروژه
def get_role(db: Session, project_id: int, person_id: int) -> Optional[str]:
    member = db.execute(
        select(ProjectMembers.AccessType).where(
            ProjectMembers.ProjectID == project_id,
            ProjectMembers.PersonID == person_id
        )
    ).scalar_one_or_none()
    return member  # ممکن است str یا None باشد


# ---- ایجاد پروژه
def create_project(
    db: Session,
    creator_person_id: int,
    data: ProjectCreate,
) -> projects:
    new_project = projects(
        **data.model_dump(exclude_none=True),
        FinishTime=datetime(2099, 12, 31, 23, 59, 59),
        RealStartTime=datetime(2099, 12, 31, 23, 59, 59),
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    # سازنده را به‌عنوان عضو مدیر اضافه کن
    new_member = ProjectMembers(
        ProjectID=new_project.ProjectID,
        PersonID=creator_person_id,
        AccessType="MANAGER",
        ParticipationPercent=100,
        CreatorID=creator_person_id,
    )
    db.add(new_member)
    db.commit()
    return new_project


# ---- ویرایش پروژه
def update_project(
    db: Session,
    project_id: int,
    data: ProjectUpdate,
) -> Optional[projects]:
    project = get_project_by_id(db, project_id)
    if not project:
        return None

    updates = data.model_dump(exclude_unset=True)
    if not updates:
        return project

    for field, value in updates.items():
        setattr(project, field, value)

    db.commit()
    db.refresh(project)
    return project


# ---- حذف منطقی پروژه
def soft_delete_project(db: Session, project_id: int) -> bool:
    project = get_project_by_id(db, project_id)
    if not project:
        return False
    project.DeleteFlag = "YES"
    db.commit()
    return True

