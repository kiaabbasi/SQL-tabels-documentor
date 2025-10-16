from typing import List, Optional
from fastapi import File, UploadFile, Form
from fastapi import APIRouter, Depends, HTTPException, Request, Header
from db.session import get_db_officedb
from db.schemas.projects import ProjectOut, ProjectCreate, ProjectUpdate
from db.schemas.ProjectMembers import ProjectMemberOut
from db.schemas.ProjectDocuments import ProjectDocumentOut, ProjectDocumentUpdate
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import Body
from core.services import projects_service as svc
from core.permissions import require_project_manager, require_project_member
from fastapi.responses import StreamingResponse
from io import BytesIO

async def optional_file(file: Optional[UploadFile] = File(None)) -> Optional[UploadFile]:
    # اگر رشته خالی اومده بود، None برگردون
    if isinstance(file, str) and file == "":
        return None
    return file


router = APIRouter()

# projects section

@router.get("/projects/{project_id}", response_model=ProjectOut, tags=["Projects"])
def get_project(project_id: int, db: Session = Depends(get_db_officedb)):
    project = svc.get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.get("/projects", response_model=List[ProjectOut], tags=["Projects"])
def list_projects(
    title: str = "",
    project_status: str = "",
    current_person_id: int = Header(..., alias="PERSON-ID"),
    db: Session = Depends(get_db_officedb),
):
    # فقط پروژه هایی که فرد عضو آنها باشد لیست می کند
    return svc.list_projects_for_person(db, current_person_id, title, project_status)

@router.post("/projects", response_model=ProjectOut, tags=["Projects"])
def create_project(request: Request, data: ProjectCreate, current_person_id: int = Header(..., alias="PERSON-ID"), db: Session = Depends(get_db_officedb)):
    return svc.create_project(db, current_person_id, data)

@router.patch("/projects/{project_id}", response_model=ProjectOut, tags=["Projects"])
def update_project(
    project_id: int,
    data: ProjectUpdate, 
    current_person_id: int = Header(..., alias="PERSON-ID"),
    db: Session = Depends(get_db_officedb)
    ):
    require_project_manager(db, project_id, current_person_id)        
    project = svc.update_project(db, project_id, data)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.delete("/projects/{project_id}", tags=["Projects"])
def soft_delete_project(project_id: int, current_person_id: int = Header(..., alias="PERSON-ID"), db: Session = Depends(get_db_officedb)):
    require_project_manager(db, project_id, current_person_id)
    ok = svc.soft_delete_project(db, project_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": f"Project {project_id} has been soft deleted"}


# project members section

@router.get("/projects/{project_id}/members/{person_id}/role", tags=["Project Members"])
def get_role(project_id: int, person_id: int, db: Session = Depends(get_db_officedb)):
    role = svc.get_role(db, project_id, person_id)
    return {"role": role}


@router.post("/projects/{project_id}/members", response_model=ProjectMemberOut, tags=["Project Members"])
def add_member_route(
    project_id: int,
    person_id: int,
    access_type: str = "MEMBER",
    current_person_id: int = Header(..., alias="PERSON-ID"),
    db: Session = Depends(get_db_officedb)
):
    require_project_manager(db, project_id, current_person_id)
    return svc.add_member(db, project_id, person_id, access_type, current_person_id)


@router.delete("/projects/{project_id}/members/{person_id}", tags=["Project Members"])
def remove_member_route(
    project_id: int,
    person_id: int,
    current_person_id: int = Header(..., alias="PERSON-ID"),
    db: Session = Depends(get_db_officedb)
):
    require_project_manager(db, project_id, current_person_id)
    ok = svc.remove_member(db, project_id, person_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Member not found")
    return {"message": "Member removed successfully"}


@router.get("/projects/{project_id}/members", response_model=List[ProjectMemberOut], tags=["Project Members"])
def get_members(project_id: int, db: Session = Depends(get_db_officedb)):
    return svc.get_members(db, project_id)


# project documents section

@router.get("/projects/{project_id}/documents", response_model=List[ProjectDocumentOut], tags=["Project Documents"])
def get_documents(project_id: int, current_person_id: int = Header(..., alias="PERSON-ID"), db: Session = Depends(get_db_officedb)):
    # --- چک عضویت کاربر ---
    role = svc.get_role(db, project_id, current_person_id)
    if role is None:
        raise HTTPException(status_code=403, detail="You must be a project member to access documents")

    return svc.get_documents(db, project_id)

@router.post("/projects/{project_id}/documents", response_model=ProjectDocumentOut, tags=["Project Documents"])
def add_document_route(
    project_id: int,
    file: UploadFile = File(...),
    description: str = None,
    doc_type_id: int = 1,
    current_person_id: int = Header(..., alias="PERSON-ID"),
    db: Session = Depends(get_db_officedb)
):
    require_project_member(db, project_id, current_person_id)
    file_content = file.file.read()

    return svc.add_document(db, project_id, current_person_id, file.filename, file_content, description, doc_type_id=doc_type_id)


@router.delete("/projects/{project_id}/documents/{document_id}", tags=["Project Documents"])
def remove_document_route(
    project_id: int,
    document_id: int,
    current_person_id: int = Header(..., alias="PERSON-ID"),
    db: Session = Depends(get_db_officedb)
):
    role = require_project_member(db, project_id, current_person_id)
    ok = svc.remove_document(db, project_id, document_id, current_person_id, role)
    if not ok:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"message": "Document removed successfully"}

@router.patch(
    "/documents/{document_id}",
    response_model=ProjectDocumentOut,
    tags=["Project Documents"]
)
def update_document_route(
    document_id: int,
    file: UploadFile | None = File(default=None), 
    description: Optional[str] = Form(None),
    doc_type_id: Optional[int] = Form(None),
    current_person_id: int = Header(..., alias="PERSON-ID"),
    db: Session = Depends(get_db_officedb),
):
    doc = svc.get_document_or_404(db, document_id)
    # چک عضویت
    role = require_project_member(db, doc.ProjectID, current_person_id)
    # آماده‌سازی تغییرات
    updates: dict = {}
    if file is not None:
        updates["FileName"] = file.filename
        updates["FileContent"] = file.file.read()
    if description is not None:
        updates["description"] = description
    if doc_type_id is not None:
        updates["ProjectDocumentTypeID"] = doc_type_id
    updated_doc = svc.update_document(db, document_id, current_person_id, role, updates)
    return updated_doc


@router.get(
    "/documents/{document_id}/download",
    tags=["Project Documents"]
)
def download_document_route(
    document_id: int,
    current_person_id: int = Header(..., alias="PERSON-ID"),
    db: Session = Depends(get_db_officedb)
):
    doc = svc.get_document_or_404(db, document_id)
    # فقط اعضای پروژه
    require_project_member(db, doc.ProjectID, current_person_id)

    return StreamingResponse(
        BytesIO(doc.FileContent),
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f"attachment; filename={doc.FileName}"
        }
    )