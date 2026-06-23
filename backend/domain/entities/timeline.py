from typing import Optional, List
from pydantic import BaseModel

class TimelineEntity(BaseModel):
    id: Optional[str] = None
