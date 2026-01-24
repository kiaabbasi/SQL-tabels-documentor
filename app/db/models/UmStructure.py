from typing import Optional

from sqlalchemy import Date, Index, String, text
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import datetime
from app.db.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class UmStructure(Base):
    __tablename__ = 'UmStructure'
    __table_args__ = (
        {'comment': 'ساختار سازمانی دانشگاه', "schema": "baseinfo"}
    )

    StructID2: Mapped[int] = mapped_column(INTEGER(10), primary_key=True, comment='کد سطح')
    StructTitle: Mapped[str] = mapped_column(String(500, 'utf8_persian_ci'), comment='عنوان')

    products: Mapped[list["products"]] = relationship(
        "products",
        back_populates="organization",
        lazy="selectin"
    )