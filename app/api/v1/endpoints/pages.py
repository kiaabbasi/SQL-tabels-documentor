from fastapi import APIRouter, HTTPException, Query,Depends
from app.core.config import settings
from app.core.services import page_service
from app.api.v1.dependencies.pagination import get_pagination
from app.core.pagination import PaginationParams

router = APIRouter(prefix="/pages", tags=["Pages"])


@router.get("/{page_name}")
def get_page_info(page_name: str):
    page = page_service.get_page(page_name)

    if page is None:
        raise HTTPException(status_code=404, detail="Page not found")

    return page
    
