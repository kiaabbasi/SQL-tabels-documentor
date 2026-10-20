from app.db.neo4j import get_driver


def fetch_table_pages_relations(table_name: str) -> list[dict] | None:
    query = """
    MATCH (t:Table {name: $table_name})

    OPTIONAL MATCH (p:Page {is_in_syspage:TRUE})-[r]-(t)

    RETURN
        p.name AS page_name,
        r.actions AS actions
    """

    with get_driver().session() as session:
        result = session.run(
            query,
            table_name=table_name,
        )

        records = list(result)

        if not records:
            return None

        return [
            {
                "page_name": record["page_name"],
                "actions": record["actions"] or [],
            }
            for record in records
            if record["page_name"] is not None
        ]
        
        
def fetch_tables(
    page: int,
    page_size: int,
) -> tuple[list[dict], bool]:
    query = """
    MATCH (t:Table)
    RETURN t AS table
    ORDER BY t.name
    SKIP $skip
    LIMIT $limit
    """

    skip = (page - 1) * page_size

    with get_driver().session() as session:
        result = session.run(
            query,
            skip=skip,
            limit=page_size + 1,
        )

        rows = [
            record["table"]._properties
            for record in result
        ]

    has_next_page = len(rows) > page_size

    return rows[:page_size], has_next_page