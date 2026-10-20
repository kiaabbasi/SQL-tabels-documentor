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
        page_size=settings.TABLES_PAGE_SIZE,)
    return {
        "tables": tables,
        "page": page,
        "page_size": settings.TABLES_PAGE_SIZE,
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

@router.get("/")
async def check_connections():
    """
    Test endpoint: verifies both database drivers can actually connect.

    Only messages that differ per database are echoed in the response;
    everything else (queries, auth) stays internal.
    """
    response: dict = {"neo4j": None, "mariadb": None}

    # --- Neo4j ---
    try:
        from app.db.neo4j import get_driver

        def _neo4j_work(tx):
            tx.run("RETURN 1 AS ping").single()

        with get_driver().session() as session:
            session.execute_write(_neo4j_work)

        response["neo4j"] = "ok"

    except Exception as e:
        response["neo4j"] = "failed"

    # --- MariaDB ---
    try:
        conn = mariadb.get_connection()

        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchall()

        response["mariadb"] = "ok"

    except Exception:
        response["mariadb"] = "failed"

    return response
