from typing import Optional, List
from pydantic import BaseModel

class MedicationEntity(BaseModel):
    id: Optional[str] = None
