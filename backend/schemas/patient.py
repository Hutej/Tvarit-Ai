from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date
from schemas.base import EntityBase
from schemas.enums import Gender

class Patient(EntityBase):
    first_name: str
    last_name: str
    dob: date
    gender: Gender
    mrn: Optional[str] = None
    address: Optional[str] = None
    contact_number: Optional[str] = None
    family_history: List[str] = Field(default_factory=list)
    social_history: List[str] = Field(default_factory=list)
    risk_factors: List[str] = Field(default_factory=list)
