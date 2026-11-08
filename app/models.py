from datetime import date
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class AuditStatus(str, Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class AuditBase(BaseModel):
    audit_number: str = Field(..., min_length=1, max_length=20, description="Номер аудита")
    department: str = Field(..., min_length=1, max_length=150, description="Проверяемое подразделение")
    scope: str = Field(..., min_length=1, max_length=250, description="Область аудита")
    criteria: str = Field(..., min_length=1, max_length=250, description="Критерии аудита")
    planned_date: date = Field(..., description="Плановая дата проведения")
    actual_date: Optional[date] = Field(None, description="Фактическая дата проведения")
    status: AuditStatus = Field(AuditStatus.PLANNED, description="Статус аудита")
    lead_auditor: str = Field(..., min_length=1, max_length=150, description="Ведущий аудитор")
    auditors: List[str] = Field(default_factory=list, description="Состав аудиторской группы")
    notes: Optional[str] = Field(None, max_length=500, description="Примечания")


class AuditCreate(AuditBase):
    pass


class Audit(AuditBase):
    id: int = Field(..., description="Уникальный идентификатор аудита")

    class Config:
        from_attributes = True