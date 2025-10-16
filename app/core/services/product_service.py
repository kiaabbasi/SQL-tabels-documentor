from sqlalchemy.orm import Session, joinedload
from db.models.products import products
from db.schemas.product import ProductCreate, ProductUpdate

def get_product_by_id(db: Session, product_id: int):
    """
    واکشی یک محصول با ID
    """
    return db.query(products).filter(products.ProductID == product_id, products.isDeleted==False).first()

def get_scrum_role(db: Session, product_id: int, person_id: int):
    """
    نقش اسکرام یک فرد در یک محصول
    """
    return "PRODUCT_OWNER"


def create_product(db: Session, product: ProductCreate, creator_id: int):
    db_product = products(**product.model_dump(), CreatedBy=creator_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product

def get_products(db: Session, skip: int = 0, limit: int = 100):
        return (
        db.query(products)
        .filter(products.isDeleted == False)
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_product(db: Session, product_id: int):
    return db.query(products).filter(products.ProductID == product_id, products.isDeleted==False).first()

def update_product(db: Session, product_id: int, product: ProductUpdate):
    db_product = db.query(products).filter(products.ProductID == product_id).first()
    if not db_product:
        return None
    for key, value in product.model_dump(exclude_unset=True).items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = db.query(products).filter(products.ProductID == product_id).first()
    if not db_product:
        return None
    db_product.isDeleted = True
    db.commit()
    db.refresh(db_product)
    return db_product

