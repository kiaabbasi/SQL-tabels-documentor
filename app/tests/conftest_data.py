import json
import pytest
from pathlib import Path
from sqlalchemy.orm import Session
from db.models.products import products
from db.models.sprints import sprints
from db.models.ProductDoD import ProductDoD
from db.models.UserStories import UserStories, StoryStatusEnum
from db.models.ScrumUserRole import ScrumUserRole
from .conftest_clean import make_clean_fixture

DATA_DIR = Path(__file__).parent / "data"

def load_json_data(file_name: str):
    with open(DATA_DIR / file_name, "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.fixture
def seed_reports_data(db_session: Session, clean_project_data):
    """
    Seed کردن داده‌های reports.json بعد از پاک‌سازی جداول
    (به جز رکوردهای ثابت).
    """

    data = load_json_data("reports.json")
    inserted = {"products": [], "sprints": [], "userstories": []}

    # --------------------
    # Products
    # --------------------
    for p in data.get("products", []):
        obj = products(**p)
        db_session.add(obj)
        db_session.commit()
        db_session.refresh(obj)
        inserted["products"].append(obj)

    # --------------------
    # Sprints
    # --------------------
    for sp in data.get("sprints", []):
        obj = sprints(**sp)
        db_session.add(obj)
        db_session.commit()
        db_session.refresh(obj)
        inserted["sprints"].append(obj)

    # Index
    products_by_name = {p.name: p for p in inserted["products"]}
    sprints_by_title = {sp.title: sp for sp in inserted["sprints"]}

    # --------------------
    # UserStories
    # --------------------
    for us in data.get("userstories", []):
        product_name = us.pop("product_name")
        sprint_title = us.pop("sprint_title")

        product = products_by_name.get(product_name)
        sprint = sprints_by_title.get(sprint_title)

        if not product:
            raise ValueError(f"Product '{product_name}' not found in inserted products")
        if not sprint:
            raise ValueError(f"Sprint '{sprint_title}' not found in inserted sprints")

        us["ProductID"] = product.ProductID
        us["SprintID"] = sprint.SprintID
        us["status"] = StoryStatusEnum[us["status"]]

        obj = UserStories(**us)
        db_session.add(obj)
        db_session.commit()
        db_session.refresh(obj)
        inserted["userstories"].append(obj)

    yield inserted
