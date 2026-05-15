from pydantic import Field
from pydantic_settings import BaseSettings

ONE_DAY_IN_HOURS = 60 * 24

class Settings(BaseSettings):
    DATABASE_URL: str = Field(
        ...,
        env="DATABASE_URL"
    )
    JWT_SECRET: str = Field(
        ...,
        env="JWT_SECRET"
    )
    JWT_ALGORITHM: str = Field(
        default="HS256",
        env="JWT_ALGORITHM"
    )
    JWT_EXPIRES_MIN: int = Field(
        default=ONE_DAY_IN_HOURS,
        env="JWT_EXPIRES_MIN"
    )
    PROJECT_NAME: str = "Devinote"
    ENVIRONMENT: str = Field(
        ...,
        env="ENVIRONMENT"
    )
    
    class Config:
        env_file = ".env"
        
settings = Settings()