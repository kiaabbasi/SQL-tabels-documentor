from fastapi import APIRouter, HTTPException, Query,Depends
from app.core.config import settings
from app.core.services import table_service
from app.api.v1.dependencies.pagination import get_pagination
from app.core.pagination import PaginationParams

router = APIRouter(prefix="/tables", tags=["Tables"])


@router.get("/")
async def get_tables(
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
):
    tables, has_next = table_service.get_all_tables(
        page=page,
        page_size=settings.PAGINATIONSIZE,)
    return {
        "tables": tables,
        "page": page,
        "page_size": settings.PAGINATIONSIZE,
        "has_next": has_next,
    }


@router.get("/without-description/")
async def get_tables_without_description(pagination: PaginationParams = Depends(get_pagination),):
    tables = table_service.get_tables_without_description_service(limit = pagination.limit, offset = pagination.offset)
    return {
        "tables": tables['items'],
        'has_next' : tables['has_more_page']
    }


@router.get("/fields/without-description/")
async def get_fields_without_description(pagination: PaginationParams = Depends(get_pagination)):
    fields = table_service.get_fields_without_description_service(limit = pagination.limit, offset = pagination.offset)
    return {
        "fields": fields,
    }


@router.get("/field-data-mappings/without-description/")
async def get_field_data_mappings_without_show_value(pagination: PaginationParams = Depends(get_pagination)):
    mappings = table_service.get_field_data_mappings_without_show_value_service(limit = pagination.limit, offset = pagination.offset)
    return {
        
        "field_data_mappings": mappings,
    }


@router.get("/{table_name}/field-data-mappings/")
async def get_field_data_mappings(table_name: str):
    mappings = table_service.get_field_data_mappings_service(table_name)
    return {
        "table": table_name,
        "field_data_mappings": mappings,
    }


@router.get("/{table_name}/relations/")
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

@router.get("/{table_name}/fields/")
async def get_table_fields(table_name: str):
    fields = table_service.get_table_fields_service(table_name)
    return {
        "table": table_name,
        "fields": fields,
    }


@router.get("/{table_name}/info/")
async def get_table_information(table_name: str):
    information = table_service.get_table_information_service(table_name)
    if information is None:
        raise HTTPException(status_code=404, detail=f"Table '{table_name}' does not exist.")
    return information