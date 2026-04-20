from pydantic import BaseModel, Field
from typing import List, Optional


class Patient(BaseModel):
    age: Optional[int] = None
    gender: Optional[str] = None


class Clinical(BaseModel):
    diagnosis_codes: Optional[List[str]] = Field(default_factory=list)
    procedure_codes: Optional[List[str]] = Field(default_factory=list)
    notes: Optional[str] = None


class Document(BaseModel):
    type: str
    content: Optional[str] = None


class Payer(BaseModel):
    payer_id: Optional[str] = None
    policy_type: Optional[str] = None


class InputRequest(BaseModel):
    patient: Optional[Patient] = None
    clinical: Optional[Clinical] = None
    documents: Optional[List[Document]] = Field(default_factory=list)
    payer: Optional[Payer] = None

    class Config:
        extra = "allow"