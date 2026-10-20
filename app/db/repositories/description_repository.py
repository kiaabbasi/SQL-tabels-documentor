from app.core.config import settings
from app.db.mariadb import fetch_rows

# A description counts as "missing" when it is NULL, an empty string,
# or the placeholder text "نامشخص" (unknown).
_EMPTY_DESCRIPTION = "(description IS NULL OR description = '' OR description = 'نامشخص')"


def fetch_tables_without_description() -> list[dict]:
    """Fetch every MIS_Tables row whose description is empty."""
    query = f"""
    SELECT * FROM `{settings.MARIADB_DATABASE}`.`MIS_Tables`
    WHERE {_EMPTY_DESCRIPTION}
    ORDER BY name
    """

    return fetch_rows(query)


def fetch_field_data_mappings_without_show_value() -> list[dict]:
    """Fetch every FieldDataMappings row whose ShowValue is empty."""
    query = f"""
    SELECT * FROM `{settings.MARIADB_DATABASE}`.`FieldDataMappings`
    WHERE {_EMPTY_DESCRIPTION}
    """

    return fetch_rows(query)


def fetch_fields_without_description() -> list[dict]:
    """Fetch every MIS_TableFields row whose description is empty."""
    query = f"""
    SELECT * FROM `{settings.MARIADB_DATABASE}`.`MIS_TableFields`
    WHERE {_EMPTY_DESCRIPTION}
    """

    return fetch_rows(query)
