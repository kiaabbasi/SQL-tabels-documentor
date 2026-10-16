from fastapi import APIRouter, HTTPException
from app.core.services import table_service

router = APIRouter(prefix="/tables", tags=["Tables"])


@router.get("/")
async def get_tables():
    return {"tables": []}


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
