from pydantic import BaseModel, model_validator, ConfigDict, computed_field
from typing import Optional, Literal
from db.enums import PROJECT_STATUS_LABELS
from datetime import datetime
from utils.datetime_helper import to_jalali_datetime


class ProjectOut(BaseModel):
    ProjectID: int
    ouid: int
    title: str
    description: str
    StartTime: Optional[datetime] = None
    EndTime: Optional[datetime] = None
    SysCode: int
    ProjectPriority: int
    FacCode: int
    ProjectStatus: str

    # --- فیلدهای کمکی ---
    @computed_field
    def ProjectStatusLabel(self) -> str:
        return PROJECT_STATUS_LABELS.get(self.ProjectStatus)

    @computed_field
    def StartTimeJalali(self) -> Optional[str]:
        return to_jalali_datetime(self.StartTime)

    @computed_field
    def EndTimeJalali(self) -> Optional[str]:
        return to_jalali_datetime(self.EndTime)

    model_config = ConfigDict(from_attributes=True)


class ProjectCreate(BaseModel):
    ouid: int
    title: str
    description: str
    StartTime: datetime
    EndTime: datetime
    SysCode: int
    ProjectPriority: int
    FacCode: int

    model_config = ConfigDict(from_attributes=True)


class ProjectUpdate(BaseModel):
    ouid: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    StartTime: Optional[datetime] = None
    EndTime: Optional[datetime] = None
    SysCode: Optional[int] = None
    ProjectPriority: Optional[int] = None
    ProjectStatus: Optional[
        Literal[
            'NOT_STARTED',
            'DEVELOPING',
            'MAINTENANCE',
            'FINISHED',
            'SUSPENDED',
            'FINISHED_BY_DEBT',
            'CONTINUOUS'
        ]
    ] = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid"
    )

    @model_validator(mode="after")
    def check_time_order(self):
        if self.StartTime and self.EndTime and self.EndTime < self.StartTime:
            raise ValueError("EndTime نمی‌تواند قبل از StartTime باشد.")
        return self
