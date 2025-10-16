from core.logging_config import logger
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from api.v1.endpoints import (products_base,
                              common,
                              )
from middlewares.middleware import RequestContextMiddleware
import db.models

# app = FastAPI(title="FUM FastAPI Skeleton", version="1.0.0")
ROOT_PATH = os.getenv("ROOT_PATH", "/fastapi-projectmanagement")

app = FastAPI(
    title="FUM FastAPI Skeleton",
    version="1.0.0",
    root_path=ROOT_PATH,           # مهم برای ساخت درست URLها (docs, openapi, ...)
    docs_url="/docs",              # آدرس داخلی اپ؛ بیرونی: <host>/<root_path>/docs
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)
logger.info("🚀 Application starting...")

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
app.include_router(products_base.router, prefix="/api/v1")
app.include_router(common.router, prefix="/api/v1/common")

@app.get("/health")
async def health():
    return {" OK ": True}
