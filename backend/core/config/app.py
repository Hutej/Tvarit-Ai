from pydantic import Field
from pydantic_settings import BaseSettings

class AppConfig(BaseSettings):
    environment: str = Field(default="development")
