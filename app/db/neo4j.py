from neo4j import GraphDatabase

from app.core.config import settings

_driver = None


def get_driver():
    """Lazy singleton: the driver is created only on first use,
    so the app can start even when NEO4J_* env vars are not set yet."""
    global _driver
    if _driver is None:
        if not settings.NEO4J_ADDRESS:
            raise RuntimeError(
                "NEO4J_ADDRESS / NEO4J_USERNAME / NEO4J_PASSWORD are not set in .env"
            )
        _driver = GraphDatabase.driver(
            settings.NEO4J_ADDRESS,
            auth=(
                settings.NEO4J_USERNAME,
                settings.NEO4J_PASSWORD,
            ),
        )
    return _driver
