from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.db.session import get_db_officedb
from app.db.schemas.product import ProductCreate, ProductOut, ProductUpdate
from app.core.services import product_service, common_service
from app.core.permissions import require_product_role_admin

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductOut)
def create_product(
    product: ProductCreate,
    current_person_id: int = Header(..., alias="PERSON-ID"),
    db: Session = Depends(get_db_officedb)
):
    res = product_service.create_product(db, product, current_person_id)
    db.refresh(res)
    return res

@router.get("/", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db_officedb)):
    return product_service.get_products(db)

@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db_officedb)):
    db_product = product_service.get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.put("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    product: ProductUpdate,
    current_person_id: int = Header(..., alias="PERSON-ID"),
    db: Session = Depends(get_db_officedb)
):
    require_product_role_admin(db, product_id, current_person_id)
    db_product = product_service.update_product(db, product_id, product)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.refresh(db_product)
    return db_product

@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    current_person_id: int = Header(..., alias="PERSON-ID"),
    db: Session = Depends(get_db_officedb)
):
    require_product_role_admin(db, product_id, current_person_id)    
    db_product = product_service.delete_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "product removed successfully"}
