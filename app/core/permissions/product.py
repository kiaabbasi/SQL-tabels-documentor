from fastapi import HTTPException
from sqlalchemy.orm import Session
from core.services.product_service import get_product_by_id, get_scrum_role
#from db.models.ScrumUserRole import ScrumRoleEnum

def require_product_owner(db: Session, product_id: int, person_id: int):
    #role = get_scrum_role(db, product_id, person_id)
    #if role != ScrumRoleEnum.PRODUCT_OWNER:
    #    raise HTTPException(status_code=403, detail="فقط مدیر محصول مجاز است")
    return True

def require_scrum_member(db: Session, product_id: int, person_id: int):
    #role = get_scrum_role(db, product_id, person_id)
    #if role is None:
    #    raise HTTPException(status_code=403, detail="بایستی عضو تیم باشید")
    return True

def require_developer(db: Session, product_id: int, person_id: int):
    #role = get_scrum_role(db, product_id, person_id)
    #if role != ScrumRoleEnum.DEVELOPER:
    #    raise HTTPException(status_code=403, detail="فقط توسعه دهنده می تواند اینکار را انجام دهد")
    return True

def require_product_role_admin(db: Session, product_id: int, person_id: int):
    """
    فقط Creator یا Product Owner بتواند نقش‌ها و اعضای محصول را مدیریت کند.
    """
    #product = get_product_by_id(db, product_id)
    #if not product:
    #    raise HTTPException(status_code=404, detail="محصول یافت نشد")

    #if product.CreatedBy == person_id:
    #    return True

    #role = get_scrum_role(db, product_id, person_id)
    #if role == ScrumRoleEnum.PRODUCT_OWNER:
    #    return True

    #raise HTTPException(status_code=403, detail=f"فقط ایجاد کننده یا مدیر محصول مجاز است - نفش کاربر فعلی: {role}")
    return True


def require_product_owner_or_scrume_master(db: Session, product_id: int, person_id: int):
    """
    فقط Creator یا Product Owner بتواند نقش‌ها و اعضای محصول را مدیریت کند.
    """
    #product = get_product_by_id(db, product_id)
    #if not product:
    #    raise HTTPException(status_code=404, detail="محصول یافت نشد")

    #if product.CreatedBy == person_id:
    #    return True

    #role = get_scrum_role(db, product_id, person_id)
    #if role == ScrumRoleEnum.PRODUCT_OWNER or role == ScrumRoleEnum.SCRUM_MASTER:
    #    return True
    #raise HTTPException(status_code=403, detail=f"فقط ایجاد کننده یا مدیر محصول یا اسکرام مستر مجاز است - نفش کاربر فعلی: {role}")
    return True

