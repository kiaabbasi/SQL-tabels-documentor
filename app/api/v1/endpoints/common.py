from typing import List
from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from db.session import get_db_officedb
from core.services import common_service as svc

router = APIRouter()

@router.get("/org-units", tags=["Common"])
def get_org_main_units(db: Session = Depends(get_db_officedb)):
    """
    دریافت فهرست واحدهای اصلی سازمانی (برای انتخاب در UI)
    """
    return svc.list_org_main_units(db)

@router.get("/team-members", tags=["Common"])
def get_team_members(db: Session = Depends(get_db_officedb)):
    """
    دریافت فهرست اعضای تیم‌ها (برای استفاده در autocomplete)
    """
    return svc.list_team_members(db)

@router.get("/products", tags=["Common"])
def get_products_for_combo(
    current_person_id: int = Header(..., alias="PERSON-ID"),
    db: Session = Depends(get_db_officedb)
):
    """
    دریافت لیست محصولاتی که کاربر عضو آنهاست (برای کمبوباکس)
    """
    return svc.list_products(db, current_person_id)