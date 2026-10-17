from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# .env lives next to this package: app/.env
BASE_DIR = Path(__file__).resolve().parent.parent  # .../app

load_dotenv(str(BASE_DIR / ".env"), encoding="utf-8")

class Settings(BaseSettings):


    # Neo4j config
    NEO4J_ADDRESS: str | None = None
    NEO4J_USERNAME: str | None = None
    NEO4J_PASSWORD: str | None = None

    mariadb_address : str | None =None
    mariadb_root_password: str | None =None
    debug: bool  =True
    model_config = SettingsConfigDict(env_file=str(BASE_DIR / ".env"), extra="ignore")


settings = Settings()
