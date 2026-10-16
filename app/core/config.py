from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
import os
load_dotenv(encoding="utf-8")

class Settings(BaseSettings):
    APP_ENV: str = "dev"

    # مسیر ذخیره فایل‌ها
    DEV_ACTIVITY_STORAGE_PATH: str | None = None
    DEV_DOCUMENT_STORAGE_PATH: str | None = None
    
    PROD_ACTIVITY_STORAGE_PATH: str | None = None
    PROD_DOCUMENT_STORAGE_PATH: str | None = None

    # DEV config
    DEV_HOST: str | None = None
    DEV_PORT: str | None = None
    DEV_USER: str | None = None
    DEV_PASSWORD: str | None = None
    DEV_DB_FRAMEWORK: str | None = None
    DEV_DB_PROJECTMANAGEMENT: str | None = None

    # MASTER config
    MASTER_HOST: str | None = None
    MASTER_PORT: str | None = None
    MASTER_USER: str | None = None
    MASTER_PASSWORD: str | None = None
    MASTER_DB_FRAMEWORK: str | None = None
    # OFFICE DB config
    OFFICEDB_HOST: str | None = None
    OFFICEDB_PORT: str | None = None
    OFFICEDB_USER: str | None = None
    OFFICEDB_PASSWORD: str | None = None
    OFFICEDB_DB_PROJECTMANAGEMENT: str | None = None

    # Neo4j config
    NEO4J_ADDRESS: str | None = None
    NEO4J_USERNAME: str | None = None
    NEO4J_PASSWORD: str | None = None

    # SLAVE config
    SLAVE_HOST: str | None = None
    SLAVE_PORT: str | None = None
    SLAVE_USER: str | None = None
    SLAVE_PASSWORD: str | None = None
    SLAVE_DB_FRAMEWORK: str | None = None

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

# ساخت DB_CONFIGS بر اساس محیط
if settings.APP_ENV == "dev":
    ACTIVITY_STORAGE_PATH = settings.DEV_ACTIVITY_STORAGE_PATH
    DOCUMENT_STORAGE_PATH = settings.DEV_DOCUMENT_STORAGE_PATH
    # همه دیتابیس‌ها روی یک سرور DEV
    DB_CONFIGS = {
        "dev": {
            "DB_HOST": settings.DEV_HOST,
            "DB_PORT": settings.DEV_PORT,
            "DB_USER": settings.DEV_USER,
            "DB_PASSWORD": settings.DEV_PASSWORD,
        }
    }
else:  # prod
    ACTIVITY_STORAGE_PATH = settings.PROD_ACTIVITY_STORAGE_PATH
    DOCUMENT_STORAGE_PATH = settings.PROD_DOCUMENT_STORAGE_PATH
    DB_CONFIGS = {
        "master": {
            "DB_HOST": settings.MASTER_HOST,
            "DB_PORT": settings.MASTER_PORT,
            "DB_USER": settings.MASTER_USER,
            "DB_PASSWORD": settings.MASTER_PASSWORD,
            "DB_NAME": settings.MASTER_DB_FRAMEWORK,
        },
        "officedb": {
            "DB_HOST": settings.OFFICEDB_HOST,
            "DB_PORT": settings.OFFICEDB_PORT,
            "DB_USER": settings.OFFICEDB_USER,
            "DB_PASSWORD": settings.OFFICEDB_PASSWORD,
            "DB_NAME": "projectmanagement",
        },
        "slave": {
            "DB_HOST": settings.SLAVE_HOST,
            "DB_PORT": settings.SLAVE_PORT,
            "DB_USER": settings.SLAVE_USER,
            "DB_PASSWORD": settings.SLAVE_PASSWORD,
            "DB_NAME": "framework",
        },
    }
