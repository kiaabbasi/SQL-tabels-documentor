from app.db.repositories import page_repository


def get_page(name: str) -> dict | None:
    return page_repository.fetch_page(name)