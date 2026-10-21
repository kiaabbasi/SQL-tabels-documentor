from app.db.neo4j import get_driver


def fetch_page(page_name: str) -> dict | None:
    """Fetch the Page node with the given name, or None if it does not exist."""
    query = """
    MATCH (p:Page {name: $page_name})
    RETURN p
    """

    with get_driver().session() as session:
        result = session.run(query, page_name=page_name)
        record = result.single()

        if record is None:
            return None

        return dict(record["p"])