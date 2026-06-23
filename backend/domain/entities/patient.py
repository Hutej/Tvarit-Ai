from typing import Optional, List
from pydantic import BaseModel

class PatientEntity(BaseModel):
    id: Optional[str] = None
