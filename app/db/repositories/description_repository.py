from app.core.config import settings
from app.db.mariadb import fetch_rows

# A description counts as "missing" when it is NULL, an empty string,
# or the placeholder text "نامشخص" (unknown).
_EMPTY_DESCRIPTION = "({0} IS NULL OR {0} = '' OR {0} = 'نامشخص')"


def _fetch_page(
    table: str,
    column: str,
    order_by: str,
    limit: int | None = None,
    offset: int | None = None,
) -> dict:
    """Select rows of `table` where `column` is empty, with optional limit/offset.

    If limit and offset are not set, all rows are returned.
    Returns {"items": [...], "has_more_page": bool}.
    """
    query = f"""
    SELECT * FROM `{settings.MARIADB_DATABASE}`.`{table}`
    WHERE {_EMPTY_DESCRIPTION.format(column)}
    ORDER BY {order_by}
    """

    if limit is not None:
        # Ask for one extra row to know if there is another page.
        query += f" LIMIT {int(limit) + 1}"
        if offset:
            query += f" OFFSET {int(offset)}"
    elif offset:
        # MariaDB does not allow OFFSET without LIMIT, so use the max value.
        query += f" LIMIT 18446744073709551615 OFFSET {int(offset)}"

    rows = fetch_rows(query)

    has_more_page = False
    if limit is not None and len(rows) > limit:
        has_more_page = True
        rows = rows[:limit]

    return {"items": rows, "has_more_page": has_more_page}


def fetch_tables_without_description(
    limit: int | None = None,
    offset: int | None = None,
) -> dict:
    """Fetch MIS_Tables rows whose description is empty.

    Returns {"items": [...], "has_more_page": bool}.
    """
    return _fetch_page("MIS_Tables", "description", "id", limit, offset)


def fetch_field_data_mappings_without_show_value(
    limit: int | None = None,
    offset: int | None = None,
) -> dict:
    """Fetch FieldDataMappings rows whose ShowValue is empty.

    Returns {"items": [...], "has_more_page": bool}.
    """
    return _fetch_page(
        "FieldDataMappings", "ShowValue", "FieldsDataMappingID", limit, offset
    )


def fetch_fields_without_description(
    limit: int | None = None,
    offset: int | None = None,
) -> dict:
    """Fetch MIS_TableFields rows whose description is empty.

    Returns {"items": [...], "has_more_page": bool}.
    """
    return _fetch_page("MIS_TableFields", "description", "id", limit, offset)