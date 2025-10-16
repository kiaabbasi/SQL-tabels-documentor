from typing import Optional, List

from sqlalchemy import DateTime, String, text
from sqlalchemy.dialects.mysql import BIGINT, ENUM, INTEGER, SMALLINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import datetime
from db.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

class projects(Base):
    __tablename__ = "projects"
    __table_args__ = {"schema": "projectmanagement", 'comment': 'پروژه'}

    ProjectID: Mapped[int] = mapped_column(INTEGER(10), primary_key=True)
    ouid: Mapped[int] = mapped_column(INTEGER(11), ForeignKey("baseinfo.UmStructure.StructID2"), comment='واحد سازمانی')
    ProjectGroupID: Mapped[int] = mapped_column(INTEGER(11), comment='کد گروه پروژه (کلید به جدول ProjectGroups)', default=0)
    title: Mapped[str] = mapped_column(String(500, 'utf8_persian_ci'), comment='عنوان')
    description: Mapped[str] = mapped_column(String(1000, 'utf8_persian_ci'), comment='شرح')
    StartTime: Mapped[datetime.datetime] = mapped_column(DateTime, comment='شروع')
    EndTime: Mapped[datetime.datetime] = mapped_column(DateTime, comment='پایان')
    SysCode: Mapped[int] = mapped_column(INTEGER(11), ForeignKey("framework.systems.SysCode"), comment='سیستم مربوطه')
    ProjectPriority: Mapped[int] = mapped_column(SMALLINT(6), comment='اولویت')
    ProjectStatus: Mapped[str] = mapped_column(ENUM('NOT_STARTED', 'DEVELOPING', 'MAINTENANCE', 'FINISHED', 'SUSPENDED', 'FINISHED_BY_DEBT', 'CONTINUOUS'), comment='وضعیت', default='NOT_STARTED')
    DeleteFlag: Mapped[str] = mapped_column(ENUM('YES', 'NO'), server_default=text("'NO'"), comment='فلگ حذف منطقی')
    Achievable: Mapped[str] = mapped_column(ENUM('YES', 'NO'), server_default=text("'NO'"), comment='قابل دستیابی برای کلیه اعضای دانشگاه ,هیات علمی- کارمندان و دانشجویان')
    FacCode: Mapped[int] = mapped_column(INTEGER(11), comment='با تعیین کد دانشکده تیکت\u200cهای مربوط به سؤالات آموزشی دانشجویان دانشکده به طور مستقیم به پاسخگویان این پروژه ارجاع می\u200cشود. پس پاسخگویان چنین پروژه\u200cای باید کارشناسان آموزشی آن دانشکده باشند.', default=0)
    cost: Mapped[int] = mapped_column(BIGINT(20), comment='هزینه پیش بینی شده', default=0)
    PMOSupervision: Mapped[str] = mapped_column(ENUM('YES', 'NO'), server_default=text("'NO'"), comment='تحت نظارت PMO')
    MngUniSupervision: Mapped[str] = mapped_column(ENUM('YES', 'NO'), server_default=text("'NO'"), comment='تحت نظارت رئیس دانشگاه')
    ProjectSponsor: Mapped[int] = mapped_column(INTEGER(11), comment='مجری پروژه', default=0)
    FinishTime: Mapped[datetime.datetime] = mapped_column(DateTime, comment='تاریخ خاتمه')
    ProgressReport: Mapped[int] = mapped_column(INTEGER(11), comment='بازه ارائه گزارش پیشرفت', default=0)
    ApplicationPlanID: Mapped[int] = mapped_column(INTEGER(10), comment='کلید جدول طرح پژوهش برون دانشگاهی ApplicationPlan', default=0)
    ResearchPlanID: Mapped[int] = mapped_column(INTEGER(10), comment='کلید جدول  طرح پژوهش درون دانشگاهی ResearchPlans', default=0)
    RealStartTime: Mapped[datetime.datetime] = mapped_column(DateTime, comment='تاریخ شروع واقعی')
    ResSuspended: Mapped[Optional[str]] = mapped_column(String(500, 'utf8_persian_ci'), comment='دلیل تعلیق پروژه', default='')
    ExtOuid: Mapped[Optional[str]] = mapped_column(String(100, 'utf8_persian_ci'), comment='کارفرما بیرونی', default='')
    ExtSponser: Mapped[Optional[str]] = mapped_column(String(100, 'utf8_persian_ci'), comment='مجری بیرونی', default='')
    TypeProject: Mapped[Optional[int]] = mapped_column(SMALLINT(2), comment='نوع پروژه', default=0)
    NatureProject: Mapped[Optional[str]] = mapped_column(ENUM('INCOME', 'COST'), comment='ماهیت پروژه\nدرامدی \nسرمایه گذاری', default='INCOME')
    PlanProjectID: Mapped[Optional[int]] = mapped_column(INTEGER(11), comment='کد جدول طرح ها', default=0)
    PortfolioProjectID: Mapped[Optional[int]] = mapped_column(INTEGER(11), comment='کد جدول پورتفولیو', default=0)
    CostCurrency: Mapped[Optional[int]] = mapped_column(INTEGER(11), comment='مبلغ قرارداد ارزی', default=0)
    TypeCurrency: Mapped[Optional[int]] = mapped_column(SMALLINT(6), comment='نوع ارز', default=0)

    ou_structure: Mapped["UmStructure"] = relationship(
        "UmStructure",            
        back_populates="projects",
        lazy="joined"             
    )

    system_structure: Mapped["Systems"] = relationship(
        "Systems",             
        lazy="joined"             
    )   

    members: Mapped[List["ProjectMembers"]] = relationship(
        "ProjectMembers",
        back_populates="project",  
        lazy="selectin"
    )

    documents: Mapped[List["ProjectDocuments"]] = relationship(
        "ProjectDocuments",
        foreign_keys="[ProjectDocuments.ProjectID]",  
        lazy="selectin"
    )    

    tasks = relationship("ProjectTasks", back_populates="project")
    
    @hybrid_property
    def is_active(self) -> bool:
        return self.ProjectStatus in ["DEVELOPING", "NOT_STARTED"]

    @is_active.expression
    def is_active(cls):
        return cls.ProjectStatus.in_(["DEVELOPING", "NOT_STARTED"])
