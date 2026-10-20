from app.core.config import settings
from app.db.repositories.description_repository import (
    fetch_field_data_mappings_without_show_value,
    fetch_fields_without_description,
    fetch_tables_without_description
)
from app.db.repositories.table_repository import (
    fetch_field_data_mappings,
    fetch_table_fields,
    fetch_table_information,
    fetch_table_pages_relations,
    fetch_tables
)

def get_all_tables(page: int = 1, page_size: int = settings.TABLES_PAGE_SIZE) -> tuple[list[dict], bool]:
    return fetch_tables(page, page_size)


def get_table_relations_service(
    name: str,
) -> tuple[list[str], list[str], list[str]] | None:

    relations = fetch_table_pages_relations(name)

    if relations is None:
        return None

    read_relations: list[str] = []
    write_relations: list[str] = []
    other_relations: list[str] = []

    for relation in relations:
        page_name = relation["page_name"]
        actions = relation["actions"]

        if "Read" in actions:
            read_relations.append(page_name)

        if "Write" in actions:
            write_relations.append(page_name)

        if "Other" in actions:
            other_relations.append(page_name)

    return read_relations, write_relations, other_relations


def get_table_fields_service(name: str) -> list[dict]:
    return fetch_table_fields(name)


def get_table_information_service(name: str) -> dict | None:
    return fetch_table_information(name)


def get_tables_without_description_service() -> list[dict]:
    return fetch_tables_without_description()


def get_fields_without_description_service() -> list[dict]:
    return fetch_fields_without_description()


def get_field_data_mappings_service(name: str) -> list[dict]:
    return fetch_field_data_mappings(name)


def get_field_data_mappings_without_show_value_service() -> list[dict]:
    return fetch_field_data_mappings_without_show_value()
