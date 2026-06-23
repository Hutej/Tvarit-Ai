from typing import Dict, Optional, List, Type
from pydantic import BaseModel, Field
from agents.prompts.types import PromptMetadata, PromptVariable

class PromptTemplate(BaseModel):
    """
    Reusable template for generating prompts.
    """
    name: str
    system_template: str
    user_template: str
    variables: List[PromptVariable] = Field(default_factory=list)
    instructions: Optional[str] = None
    examples: List[str] = Field(default_factory=list)
    output_schema: Optional[Type[BaseModel]] = None
    temperature: float = Field(default=0.0, ge=0.0, le=2.0)
    metadata: PromptMetadata = Field(default_factory=PromptMetadata)
