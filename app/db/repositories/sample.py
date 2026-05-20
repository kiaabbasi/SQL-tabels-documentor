from sqlalchemy.orm import Session
from sqlalchemy import text


def get_faculty_book_authors(
    db: Session,
    fac_code: int | None = None,
    edu_grp_code: int | None = None,
    person_id: int | None = None,
):
    query = """
        SELECT * FROM BookAuthors ba
    """

    result = db.execute(
        text(query),
        {
            "fac_code": fac_code,
            "edu_grp_code": edu_grp_code,
            "person_id": person_id,
        },
    )

    return result.mappings().all()