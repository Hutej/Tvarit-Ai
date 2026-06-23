import os
from typing import Type, TypeVar, Tuple, Any
from pydantic import BaseModel
import openai
from extraction.exceptions import ProviderCommunicationException
from extraction.types import ExtractionStatistics

T = TypeVar('T', bound=BaseModel)

class OpenAIProvider:
    """
    Wrapper for OpenAI API communication utilizing Structured Outputs.
    """
    def __init__(self, model_name: str = None):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ProviderCommunicationException("OPENAI_API_KEY environment variable is not set.")
        self.client = openai.OpenAI(api_key=api_key)
        self.model_name = model_name or os.getenv("OPENAI_MODEL_NAME", "gpt-4.1")

    def generate_structured(
        self, 
        system_prompt: str, 
        user_prompt: str, 
        response_schema: Type[T]
    ) -> Tuple[T, ExtractionStatistics]:
        """
        Calls OpenAI with strict structured output.
        """
        try:
            # Using openai Beta parse for pydantic structured output
            completion = self.client.beta.chat.completions.parse(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format=response_schema,
                temperature=0.0
            )
            
            message = completion.choices[0].message
            if message.parsed:
                result = message.parsed
            else:
                raise ProviderCommunicationException("Failed to parse structured output from OpenAI.")
            
            usage = completion.usage
            stats = ExtractionStatistics(
                prompt_tokens=usage.prompt_tokens if usage else 0,
                completion_tokens=usage.completion_tokens if usage else 0,
                total_tokens=usage.total_tokens if usage else 0,
                processing_time_ms=0
            )
            
            return result, stats
            
        except Exception as e:
            raise ProviderCommunicationException(f"OpenAI API Error: {str(e)}")
