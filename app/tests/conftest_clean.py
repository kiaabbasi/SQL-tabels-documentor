import pytest
from sqlalchemy.orm import Session
from db.models.products import products
from db.models.sprints import sprints
from db.models.UserStories import UserStories

@pytest.fixture
def clean_project_data(db_session: Session):
    """
    پاک‌سازی داده‌های وابسته به پروژه (UserStories → Sprints → Products)
    با رعایت FK و حفظ رکوردهای پایه.
    """

    # رکوردهایی که باید حفظ شوند
    keep = {
        UserStories: [66],
        sprints: [],      # اگر چیزی خواستی اینجا اضافه کن
        products: [4],
    }

    def _cleanup():
        # UserStories
        pk = UserStories.__mapper__.primary_key[0]
        objs = db_session.query(UserStories).filter(~pk.in_(keep[UserStories])).all()
        for obj in objs:
            db_session.delete(obj)
        db_session.commit()

        # Sprints
        pk = sprints.__mapper__.primary_key[0]
        objs = db_session.query(sprints).filter(~pk.in_(keep[sprints])).all()
        for obj in objs:
            db_session.delete(obj)
        db_session.commit()

        # Products
        pk = products.__mapper__.primary_key[0]
        objs = db_session.query(products).filter(~pk.in_(keep[products])).all()
        for obj in objs:
            db_session.delete(obj)
        db_session.commit()

    # ---------- Setup ----------
    _cleanup()

    yield

    # ---------- Teardown ----------
    _cleanup()

# این تابع یک fixture ساز عمومی است
def make_clean_fixture(model, keep_ids: list[int] = None):
    """
    ساخت یک fixture برای پاک‌سازی جدول یک مدل
    :param model: مدل SQLAlchemy
    :param keep_ids: لیست IDهایی که نباید حذف شوند (seed data)
    """
    keep_ids = keep_ids or []

    @pytest.fixture
    def _clean_fixture(db_session: Session):
        if keep_ids:
            pk = model.__mapper__.primary_key[0]
            objs = db_session.query(model).filter(~pk.in_(keep_ids)).all()
        else:
            objs = db_session.query(model).all()

        for obj in objs:
            db_session.delete(obj)
        db_session.commit()

        yield

        # teardown هم همینطور
        if keep_ids:
            pk = model.__mapper__.primary_key[0]
            objs = db_session.query(model).filter(~pk.in_(keep_ids)).all()
        else:
            objs = db_session.query(model).all()

        for obj in objs:
            db_session.delete(obj)
        db_session.commit()

    return _clean_fixture