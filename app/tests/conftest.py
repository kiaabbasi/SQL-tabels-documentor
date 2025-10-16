import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.main import app
from db.session import get_db_officedb
from db.models.products import products
from db.models.sprints import sprints
from db.models.epics import epics
from db.models.UserStories import UserStories
from db.models.ProjectTasks import ProjectTasks
from db.models.AcceptanceCriteria import AcceptanceCriteria
from db.models.ProductDoD import ProductDoD
from db.models.ScrumUserRole import ScrumUserRole
from .conftest_clean import make_clean_fixture, clean_project_data
from .conftest_data import seed_reports_data

# ---------------------------
# تنظیمات اتصال به دیتابیس تست
# ---------------------------
DB_HOST = os.getenv("TEST_DB_HOST", "developerdb.um.ac.ir")
DB_PORT = os.getenv("TEST_DB_PORT", "3306")
DB_USER = os.getenv("TEST_DB_USER", "user1")
DB_PASSWORD = os.getenv("TEST_DB_PASSWORD", "user1")
DB_NAME = os.getenv("TEST_DB_NAME", "projectmanagement")

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ---------------------------
# override برای FastAPI
# ---------------------------
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db_officedb] = override_get_db

# ---------------------------
# Fixtures
# ---------------------------

clean_products = make_clean_fixture(products, [4])
clean_sprints = make_clean_fixture(sprints)
clean_epics = make_clean_fixture(epics, [18])
clean_userstories = make_clean_fixture(UserStories, [66])
clean_tasks = make_clean_fixture(ProjectTasks)
clean_acceptancecriteria = make_clean_fixture(AcceptanceCriteria)

clean_ProductDoD = make_clean_fixture(ProductDoD)
clean_ScrumUserRole = make_clean_fixture(ScrumUserRole)

@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client():
    return TestClient(app)

# ---------------------------
# متدهای خالی کردن جدول‌ها
# ---------------------------
def truncate_table(db, table_name: str):
    """پاک کردن تمام رکوردهای یک جدول (بدون حذف ساختار)"""
    db.execute(text(f"TRUNCATE TABLE {table_name}"))
    db.commit()

@pytest.fixture
def sample_person_id1():
    return 201309

@pytest.fixture
def sample_person_id2():
    return 365

@pytest.fixture
def sample_structure():
    return 14

@pytest.fixture
def sample_structure2():
    return 15

@pytest.fixture
def sample_product_id():
    return 4

@pytest.fixture
def sample_userstory_id():
    return 66

@pytest.fixture
def sample_epic_id():
    return 18
