from sqlalchemy.orm import Session
from sqlalchemy import text

from datetime import datetime, UTC

def list_org_main_units(db: Session):
    """
    فهرست واحدهای اصلی سازمانی (StructID2, StructTitle)
    """
    query = text("""
        select StructID2, StructTitle 
        from baseinfo.UmStructure 
        where StructParentID=1  and ValidityEndDate='0000-00-00'
        order by ordering
    """)
    result = db.execute(query).all()
    return [{"StructID2": row[0], "StructTitle": row[1]} for row in result]

def list_team_members(db: Session):
    """
    فهرست اعضای تیم‌ها (PersonID, fullname)
    """
    query = text("""
        select distinct PersonID, concat(pfname, ' ', plname) as fullname
        from projectmanagement.WorkTeamMembers
        join hrmstotal.persons on (MemberPersonID = PersonID)
        where TeamID in (19,12,8,9,36,39,28,20,35,37)
        order by plname, pfname
    """)
    result = db.execute(query).all()
    return [{"PersonID": row[0], "fullname": row[1]} for row in result]

def list_products(db: Session, person_id: int):
    """
    فهرست محصولات برای استفاده در کمبوباکس
    """
    query = text("""
        select distinct p.ProductID, p.name
        from projectmanagement.products p
        join projectmanagement.ScrumUserRoles r on r.ProductID = p.ProductID
        where r.PersonID = :pid
        order by p.name
    """)
    result = db.execute(query, {"pid": person_id}).all()
    return [{"ProductID": row[0], "name": row[1]} for row in result]