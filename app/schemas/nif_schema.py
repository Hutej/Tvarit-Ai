from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class PatientNIF(BaseModel):
    age: Optional[int]
    gender: Optional[str]


class ClinicalNIF(BaseModel):
    diagnosis_codes: List[str] = []
    procedure_codes: List[str] = []
    notes: Optional[str]
    extracted: dict


class DocumentNIF(BaseModel):
    type: str
    status: str


class NIF(BaseModel):
    request_id: str

    patient: PatientNIF
    clinical: ClinicalNIF
    documents: List[DocumentNIF]
    payer: dict

    metadata: dict