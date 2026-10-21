from fastapi import Query
from app.core.config import settings
from app.core.pagination import PaginationParams


def get_pagination(
    page: int = Query(default=1, ge=1),
) -> PaginationParams:
    return PaginationParams(
        page=page,
        page_size=settings.PAGINATIONSIZE,
    )