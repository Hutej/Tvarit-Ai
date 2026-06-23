from typing import Type, TypeVar, Tuple
from pydantic import BaseModel
from core.ai.providers.openai_provider import OpenAIProvider
from extraction.types import ExtractionStatistics

T = TypeVar('T', bound=BaseModel)

class AIClient:
    """
    Reusable AI client that abstracts the underlying provider.
    """
    def __init__(self):
        self.provider = OpenAIProvider()

    def generate_structured(
        self, 
        system_prompt: str, 
        user_prompt: str, 
        response_schema: Type[T]
    ) -> Tuple[T, ExtractionStatistics]:
        """
        Accepts prompts and schema, delegates to provider, returns validated object.
        """
        return self.provider.generate_structured(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_schema=response_schema
        )
