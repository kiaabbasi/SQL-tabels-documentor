from fastapi import APIRouter, HTTPException, Query
from app.core.config import settings
from app.core.services import table_service

router = APIRouter(prefix="/tables", tags=["Tables"])


@router.get("/")
async def get_tables(
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
):
    tables, has_next = table_service.get_all_tables(
        page=page,
        page_size=settings.tables_page_size,
    )
    return {
        "tables": tables,
        "page": page,
        "page_size": settings.tables_page_size,
        "has_next": has_next,
    }


@router.get("/getreleations/{table_name}")
async def get_table_relations(table_name: str):
    relations = table_service.get_table_relations_service(table_name)
    if relations is None:
        raise HTTPException(status_code=404, detail=f"Table '{table_name}' does not exist.")
    read, write, other = relations
    return {
        "table": table_name,
        "read": read,
        "write": write,
        "other": other,
    }
