from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from schemas.base import EntityBase

class TimelineEvent(EntityBase):
    date: datetime
    event_type: str
    description: str
    related_entity_ids: List[str] = Field(default_factory=list)
