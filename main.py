from app.core.logging_config import logger
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import tables,pages
from app.middlewares.middleware import RequestContextMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
import app.db.models

# app = FastAPI(title="FUM FastAPI Skeleton", version="1.0.0")
ROOT_PATH = os.getenv("ROOT_PATH", "/fastapi-projectmanagement")
logger.info("🚀 Application starting...")

app = FastAPI(
    docs_url=None,   # برای آفلاین کردن swagger که به جای گرفتن از cdn از local بگیرد. در صورت عدم نیاز برداشته شود
    redoc_url=None,
)
# برای آفلاین کردن swagger که به جای گرفتن از cdn از local بگیرد. در صورت عدم نیاز برداشته شود
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/docs", include_in_schema=False)
def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="API Docs",
        swagger_js_url="/static/swagger/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger/swagger-ui.css",
    )

# Enable CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Define another middleware to apply our custom dependencies
app.add_middleware(RequestContextMiddleware)
app.include_router(tables.router, prefix="/api/v1")
app.include_router(pages.router,prefix="/api/v1")
@app.get("/health")
async def health():
    return {" OK ": True}
