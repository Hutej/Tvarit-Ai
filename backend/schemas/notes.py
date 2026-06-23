from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from schemas.base import EntityBase

class ClinicalNote(EntityBase):
    title: str
    text: str
    date: datetime
    author_id: Optional[str] = None

class ProgressNote(ClinicalNote):
    pass

class OperativeNote(ClinicalNote):
    pre_op_diagnosis: Optional[str] = None
    post_op_diagnosis: Optional[str] = None
    procedure_details: Optional[str] = None

class PathologyReport(ClinicalNote):
    specimen: Optional[str] = None
    macroscopic_description: Optional[str] = None
    microscopic_description: Optional[str] = None

class DischargeSummary(ClinicalNote):
    admission_date: Optional[datetime] = None
    discharge_date: Optional[datetime] = None
    discharge_disposition: Optional[str] = None

class Referral(EntityBase):
    referring_provider_id: str
    target_provider_id: Optional[str] = None
    target_specialty: Optional[str] = None
    reason: str
    date: datetime
