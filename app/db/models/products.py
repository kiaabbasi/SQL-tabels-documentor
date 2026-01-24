from sqlalchemy import String, Integer, Date, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, UTC
from app.db.base import Base
import enum
from sqlalchemy import Enum as SAEnum

class ProductStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    RETIRED = "RETIRED"
    DRAFT = "DRAFT"

class products(Base):
    __tablename__ = "products"
    __table_args__ = {"schema": "projectmanagement"}

    ProductID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    isDeleted: Mapped[bool] = mapped_column(default=False, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(1024))
    launchDate: Mapped[datetime] = mapped_column(Date, nullable=True)   # تاریخ لانچ محصول
    status: Mapped[ProductStatus] = mapped_column(
        SAEnum(ProductStatus, name="productstatus"), 
        default=ProductStatus.ACTIVE
    )

    StructID2: Mapped[int] = mapped_column(ForeignKey("baseinfo.UmStructure.StructID2"), nullable=False)
    
    CreatedBy: Mapped[int] = mapped_column(ForeignKey("hrmstotal.persons.PersonID"), nullable=False)
    CreatedAt: Mapped[datetime] = mapped_column(default=datetime.now(UTC))
    
    organization = relationship("UmStructure", back_populates="products")
    #epics: Mapped[list["epics"]] = relationship("epics", back_populates="product", cascade="all, delete-orphan", passive_deletes=True)
    #userStories: Mapped[list["UserStories"]] = relationship("UserStories", back_populates="product", cascade="all, delete-orphan", passive_deletes=True)
    #scrumRoles: Mapped[list["ScrumUserRole"]] = relationship("ScrumUserRole", back_populates="product", cascade="all, delete-orphan")
    
    creator: Mapped["Persons"] = relationship(
        "Persons",
        lazy="joined",       
        innerjoin=False,     
        viewonly=True,       
    )


