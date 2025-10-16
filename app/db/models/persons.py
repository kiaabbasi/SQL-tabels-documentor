from typing import List, Optional

from sqlalchemy import DECIMAL, Date, ForeignKeyConstraint, Index, String, text
from sqlalchemy.dialects.mysql import BIGINT, FLOAT, INTEGER, SMALLINT, TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime
import decimal
from pydantic import computed_field
from db.base import Base

class Countries(Base):
    __tablename__ = 'countries'

    country_id: Mapped[int] = mapped_column(SMALLINT(6), primary_key=True)
    ptitle: Mapped[str] = mapped_column(String(50, 'utf8_persian_ci'), server_default=text("''"))
    etitle: Mapped[Optional[str]] = mapped_column(String(50, 'utf8_persian_ci'))

    #persons: Mapped[List['Persons']] = relationship('Persons', back_populates='country')


class States(Base):
    __tablename__ = 'states'

    state_id: Mapped[int] = mapped_column(SMALLINT(6), primary_key=True)
    ptitle: Mapped[str] = mapped_column(String(100, 'utf8_persian_ci'), server_default=text("''"))
    etitle: Mapped[Optional[str]] = mapped_column(String(100, 'utf8_persian_ci'))
    #RefID: Mapped[Optional[int]] = mapped_column(INTEGER(11), comment='کد پاکنا')

    cities: Mapped[List['Cities']] = relationship('Cities', back_populates='state')
    #persons: Mapped[List['Persons']] = relationship('Persons', foreign_keys='[Persons.birth_state_id]', back_populates='birth_state')
    #persons_: Mapped[List['Persons']] = relationship('Persons', foreign_keys='[Persons.issue_state_id]', back_populates='issue_state')


class Cities(Base):
    __tablename__ = 'cities'
    __table_args__ = (
        ForeignKeyConstraint(['state_id'], ['states.state_id'], name='FK_CITIES__STATES'),
        Index('FK_CITIES__STATES', 'state_id')
    )

    city_id: Mapped[int] = mapped_column(SMALLINT(6), primary_key=True)
    state_id: Mapped[int] = mapped_column(SMALLINT(6))
    ptitle: Mapped[str] = mapped_column(String(100, 'utf8_persian_ci'), server_default=text("''"))
    etitle: Mapped[Optional[str]] = mapped_column(String(100, 'utf8_persian_ci'))
    #RCoef: Mapped[Optional[float]] = mapped_column(FLOAT(9, 3), comment='ضریب منطقه')
    #RefID: Mapped[Optional[int]] = mapped_column(INTEGER(11), comment='کد پاکنا')

    state: Mapped['States'] = relationship('States', back_populates='cities')
    #persons: Mapped[List['Persons']] = relationship('Persons', foreign_keys='[Persons.birth_city_id]', back_populates='birth_city')
    #persons_: Mapped[List['Persons']] = relationship('Persons', foreign_keys='[Persons.issue_city_id]', back_populates='issue_city')


class Persons(Base):
    __tablename__ = 'persons'
    __table_args__ = (
        #ForeignKeyConstraint(['birth_city_id'], ['cities.city_id'], name='FK_PERSONS__CITIES'),
        #ForeignKeyConstraint(['birth_state_id'], ['states.state_id'], name='FK_PERSONS__STATES__1'),
        #ForeignKeyConstraint(['country_id'], ['countries.country_id'], name='FK_PERSONS__COUNTRIES'),
        #ForeignKeyConstraint(['issue_city_id'], ['cities.city_id'], name='FK_PERSONS__CITIES__2'),
        #ForeignKeyConstraint(['issue_state_id'], ['states.state_id'], name='FK_PERSONS__STATES__2'),
        #Index('CardNumber', 'RFID'),
        #Index('FK_PERSONS__CITIES', 'birth_city_id'),
        #Index('FK_PERSONS__CITIES__2', 'issue_city_id'),
        #Index('FK_PERSONS__COUNTRIES', 'country_id'),
        #Index('FK_PERSONS__STATES__1', 'birth_state_id'),
        #Index('FK_PERSONS__STATES__2', 'issue_state_id'),
        Index('PersonID_Type', 'PersonID', 'person_type'),
        #Index('national_code', 'national_code'),
        {"schema": "hrmstotal"}
    )

    PersonID: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    pfname: Mapped[str] = mapped_column(String(30, 'utf8_persian_ci'), comment='نام')
    plname: Mapped[str] = mapped_column(String(30, 'utf8_persian_ci'), comment='نام خانوادگی')
    #national_code: Mapped[str] = mapped_column(String(30, 'utf8_persian_ci'), server_default=text("' '"), comment='کد ملی')
    #CVVisible: Mapped[int] = mapped_column(SMALLINT(6), server_default=text("'0'"), comment='قابل مشاهده بودن رزومه ؟')
    #efname: Mapped[Optional[str]] = mapped_column(String(30, 'utf8_persian_ci'), comment='نام انگلیسی')
    #elname: Mapped[Optional[str]] = mapped_column(String(30, 'utf8_persian_ci'), comment='نام خانوادگی انگلیسی')
    #father_name: Mapped[Optional[str]] = mapped_column(String(30, 'utf8_persian_ci'), comment='نام پدر')
    #idcard_no: Mapped[Optional[str]] = mapped_column(String(30, 'utf8_persian_ci'), comment='شماره شناسنامه')
    #birth_date: Mapped[Optional[datetime.date]] = mapped_column(Date, comment='تاریخ تولد')
    #birth_city_id: Mapped[Optional[int]] = mapped_column(SMALLINT(6), comment='شهر محل تولد - کلید به جدول cities')
    #birth_place: Mapped[Optional[str]] = mapped_column(String(30, 'utf8_persian_ci'), comment='محل تولد')
    #issue_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    #issue_city_id: Mapped[Optional[int]] = mapped_column(SMALLINT(6), comment='شهر صدور شناسنامه - کلید به جدول cities')
    #issue_place: Mapped[Optional[str]] = mapped_column(String(30, 'utf8_persian_ci'), comment='محل صدور شناسنامه')
    #country_id: Mapped[Optional[int]] = mapped_column(SMALLINT(6), comment='کد کشور - کلید به جدول countries')
    #sex: Mapped[Optional[int]] = mapped_column(SMALLINT(6), comment='جنسیت')
    #marital_status: Mapped[Optional[int]] = mapped_column(SMALLINT(6), comment='وضعیت تاهل')
    #locality_type: Mapped[Optional[int]] = mapped_column(SMALLINT(1), comment='بومی؟')
    #address1: Mapped[Optional[str]] = mapped_column(String(255, 'utf8_persian_ci'), comment='آدرس')
    #postal_code1: Mapped[Optional[str]] = mapped_column(String(10, 'utf8_persian_ci'), comment='کد پستی')
    #home_phone1: Mapped[Optional[str]] = mapped_column(String(14, 'utf8_persian_ci'), comment='تلفن منزل')
    #address2: Mapped[Optional[str]] = mapped_column(String(255, 'utf8_persian_ci'), comment='آدرس ۲')
    #postal_code2: Mapped[Optional[str]] = mapped_column(String(10, 'utf8_persian_ci'), comment='کد پستی ۲')
    #home_phone2: Mapped[Optional[str]] = mapped_column(String(14, 'utf8_persian_ci'), comment='تلفن منزل ۲')
    #work_phone: Mapped[Optional[str]] = mapped_column(String(14, 'utf8_persian_ci'), comment='تلفن محل کار')
    #work_int_phone: Mapped[Optional[str]] = mapped_column(String(14, 'utf8_persian_ci'), comment='شماره داخلی')
    #mobile_phone: Mapped[Optional[str]] = mapped_column(String(14, 'utf8_persian_ci'), comment='تلفن همراه')
    #religion: Mapped[Optional[int]] = mapped_column(SMALLINT(6), comment='دین')
    #subreligion: Mapped[Optional[int]] = mapped_column(SMALLINT(6), comment='مذهب')
    #nationality: Mapped[Optional[int]] = mapped_column(SMALLINT(6), comment='ملیت')
    #insure_no: Mapped[Optional[str]] = mapped_column(String(20, 'utf8_persian_ci'), comment='شماره بیمه')
    #military_status: Mapped[Optional[int]] = mapped_column(SMALLINT(1), comment='وضعیت سربازی')
    #military_type: Mapped[Optional[int]] = mapped_column(SMALLINT(1), comment='نوع خدمت نظام وظیفه')
    #military_from_date: Mapped[Optional[datetime.date]] = mapped_column(Date, comment='تاریخ شروع سربازی')
    #military_to_date: Mapped[Optional[datetime.date]] = mapped_column(Date, comment='تاریخ پایان سربازی')
    #military_duration: Mapped[Optional[int]] = mapped_column(SMALLINT(2), comment='طول مدت سربازی')
    #military_comment: Mapped[Optional[str]] = mapped_column(String(255, 'utf8_persian_ci'), comment='توضیح در مورد نظام وظیفه')
    #email: Mapped[Optional[str]] = mapped_column(String(50, 'utf8_persian_ci'), comment='پست الکترونیک')
    #family_protector: Mapped[Optional[int]] = mapped_column(TINYINT(1), comment='سرپرست خانوار است؟')
    #role_student: Mapped[Optional[int]] = mapped_column(SMALLINT(1), comment='نقش دانشجو')
    #role_staff: Mapped[Optional[int]] = mapped_column(SMALLINT(1), comment='نقش کارمند')
    #role_part_time_teacher: Mapped[Optional[int]] = mapped_column(SMALLINT(1), comment='نقش استاد پاره وقت')
    #role_burse: Mapped[Optional[int]] = mapped_column(SMALLINT(1), comment='بورسیه')
    #role_other: Mapped[Optional[int]] = mapped_column(SMALLINT(1), comment='نقش متفرقه')
    #birth_state_id: Mapped[Optional[int]] = mapped_column(SMALLINT(6), comment='استان محل تولد - کلید به جدول states')
    #issue_state_id: Mapped[Optional[int]] = mapped_column(SMALLINT(6), comment='استان محل صدور شناسنامه - کلید به جدول states')
    #HomePage: Mapped[Optional[str]] = mapped_column(String(100, 'utf8_persian_ci'), comment='آدرس صفحه خانگی')
    person_type: Mapped[Optional[int]] = mapped_column(SMALLINT(6), comment='نوع استخدام')
    #idcard_serial: Mapped[Optional[str]] = mapped_column(String(15, 'utf8_persian_ci'), comment='شماره سریال شناسنامه')
    #military_duration_day: Mapped[Optional[int]] = mapped_column(SMALLINT(2), comment='طول مدت سربازی (روز)')
    #comment: Mapped[Optional[str]] = mapped_column(String(255, 'utf8_persian_ci'), comment='توضیحات')
    #transmited: Mapped[Optional[int]] = mapped_column(SMALLINT(2), comment='انتقالی است؟')
    #InsureCode: Mapped[Optional[int]] = mapped_column(INTEGER(11), comment='کد بیمه')
    #OtherPerson: Mapped[Optional[int]] = mapped_column(SMALLINT(6), comment='انواع کارکنان متفرقه')
    #TypePassport: Mapped[Optional[int]] = mapped_column(SMALLINT(6), comment='نوع گذرنامه')
    #NumPassport: Mapped[Optional[str]] = mapped_column(String(200, 'utf8_persian_ci'), comment='شماره گذرنامه')
    #SupFname: Mapped[Optional[str]] = mapped_column(String(30, 'utf8_persian_ci'), comment='نام سرپرست')
    #SupLname: Mapped[Optional[str]] = mapped_column(String(30, 'utf8_persian_ci'), comment='نام خانوادگی سرپرست')
    #StaCode: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(12, 0), comment='کد سرشماری')
    #CompanyName: Mapped[Optional[str]] = mapped_column(String(250, 'utf8_persian_ci'), comment='نام شرکت')
    #DocNo: Mapped[Optional[int]] = mapped_column(INTEGER(11), comment='شماره پرونده')
    #floor: Mapped[Optional[int]] = mapped_column(INTEGER(11), comment='طبقه')
    #RoomNo: Mapped[Optional[int]] = mapped_column(INTEGER(11), comment='شماره اتاق')
    #DeductPaid: Mapped[Optional[datetime.date]] = mapped_column(Date, comment='تاریخ کسورات پرداختی سربازی')
    #RFID: Mapped[Optional[str]] = mapped_column(String(50, 'utf8_persian_ci'))
    #ExtraNationality: Mapped[Optional[int]] = mapped_column(SMALLINT(6), comment='تابعیت مضاعف')
    #NegativeInquery: Mapped[Optional[int]] = mapped_column(SMALLINT(2), comment='استعلام منفی')
    #RefID: Mapped[Optional[int]] = mapped_column(BIGINT(20), comment='شناسه پست در پاکنا')
    #AboutMePersian: Mapped[Optional[str]] = mapped_column(String(1000, 'utf8_persian_ci'), comment='درباره من فارسی')
    #AboutMeEnglish: Mapped[Optional[str]] = mapped_column(String(1000, 'utf8_persian_ci'), comment='درباره من انگلیسی')
    #PicFileType: Mapped[Optional[str]] = mapped_column(String(250, 'utf8_persian_ci'), comment='نوع فایل عکس پرسنلی')
    #SignFileType: Mapped[Optional[str]] = mapped_column(String(250, 'utf8_persian_ci'), comment='نوع فایل امضا فرد')
    #AsaParam: Mapped[Optional[int]] = mapped_column(SMALLINT(2))

    #birth_city: Mapped[Optional['Cities']] = relationship('Cities', foreign_keys=[birth_city_id], back_populates='persons')
    #birth_state: Mapped[Optional['States']] = relationship('States', foreign_keys=[birth_state_id], back_populates='persons')
    #country: Mapped[Optional['Countries']] = relationship('Countries', back_populates='persons')
    #issue_city: Mapped[Optional['Cities']] = relationship('Cities', foreign_keys=[issue_city_id], back_populates='persons_')
    #issue_state: Mapped[Optional['States']] = relationship('States', foreign_keys=[issue_state_id], back_populates='persons_')

    @computed_field
    def fullname(self) -> Optional[str]:
        if not self.pfname or not self.plname:
            return None
        return f"{self.pfname} {self.plname}"