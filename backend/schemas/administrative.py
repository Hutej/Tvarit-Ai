from pydantic import BaseModel, Field
from typing import Optional, List
from schemas.base import EntityBase

class Provider(EntityBase):
    npi: Optional[str] = None
    first_name: str
    last_name: str
    specialty: Optional[str] = None
    contact_number: Optional[str] = None
    email: Optional[str] = None

class Organization(EntityBase):
    name: str
    npi: Optional[str] = None
    address: Optional[str] = None
    contact_number: Optional[str] = None

class Coverage(EntityBase):
    group_number: Optional[str] = None
    plan_name: Optional[str] = None
    effective_date: Optional[str] = None
    expiration_date: Optional[str] = None

class Insurance(EntityBase):
    payer_name: str
    payer_id: Optional[str] = None
    policy_number: str
    coverage: Optional[Coverage] = None
    subscriber_name: Optional[str] = None
    subscriber_dob: Optional[str] = None
