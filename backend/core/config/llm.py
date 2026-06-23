from pydantic import Field
from pydantic_settings import BaseSettings

class LLMConfig(BaseSettings):
    openai_api_key: str = Field(default="")
    model_name: str = Field(default="gpt-4o")
