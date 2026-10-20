from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# .env lives next to this package: app/.env
BASE_DIR = Path(__file__).resolve().parent.parent  # .../app

load_dotenv(str(BASE_DIR / ".env"), encoding="utf-8")

class Settings(BaseSettings):
    # Neo4j configuration
    NEO4J_ADDRESS: str | None = None
    NEO4J_USERNAME: str | None = None
    NEO4J_PASSWORD: str | None = None

    # MariaDB configuration
    MARIADB_ADDRESS: str | None = None
    MARIADB_ROOT_PASSWORD: str | None = None
    MARIADB_DATABASE: str | None = None

    # Application configuration
    DEBUG: bool = True

    # Pagination configuration
    TABLES_PAGE_SIZE: int = 50

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore",
        case_sensitive=False,
    )


settings = Settings()