import mariadb

from app.core.config import settings

_connection_pool = None


def get_connection_pool():
    """Create the MariaDB connection pool lazily."""
    global _connection_pool

    if _connection_pool is None:
        if not settings.MARIADB_ADDRESS:
            raise RuntimeError(
                "MARIADB_ADDRESS and MARIADB_ROOT_PASSWORD must be configured."
            )

        host, port = settings.MARIADB_ADDRESS.rsplit(":", 1)

        _connection_pool = mariadb.ConnectionPool(
            pool_name="fastapi_pool",
            pool_size=5,
            host=host,
            port=int(port),
            user="root",
            password=settings.MARIADB_ROOT_PASSWORD,
            database=settings.MARIADB_DATABASE,
        )

    return _connection_pool