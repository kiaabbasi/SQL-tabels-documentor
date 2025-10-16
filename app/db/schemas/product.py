from pydantic import BaseModel, ConfigDict, computed_field
from datetime import date, datetime
from enum import Enum
from typing import Optional
from .Persons import PersonBasicOut
from .UmStructure import UmStructureOut
from utils.datetime_helper import to_jalali_date, to_jalali_datetime


class ProductStatus(str, Enum):
    ACTIVE = "ACTIVE"
    RETIRED = "RETIRED"
    DRAFT = "DRAFT"


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    launchDate: Optional[date] = None
    status: ProductStatus = ProductStatus.ACTIVE
    StructID2: int   # واحد سازمانی مربوط به محصول


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    launchDate: Optional[date] = None
    status: Optional[ProductStatus] = None
    StructID2: Optional[int] = None


class ProductOut(ProductBase):
    ProductID: int
    creator: Optional[PersonBasicOut]
    organization: Optional[UmStructureOut]
    CreatedAt: Optional[datetime]

    # --- تاریخ‌های شمسی ---
    @computed_field
    def launchDateJalali(self) -> Optional[str]:
        return to_jalali_date(self.launchDate)

    @computed_field
    def CreatedAtJalali(self) -> Optional[str]:
        return to_jalali_datetime(self.CreatedAt)

    model_config = ConfigDict(from_attributes=True)
