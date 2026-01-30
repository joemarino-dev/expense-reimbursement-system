from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    # Database - can use either DATABASE_URL or individual postgres vars
    database_url: Optional[str] = None
    postgres_user: Optional[str] = None
    postgres_password: Optional[str] = None
    postgres_db: Optional[str] = None
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    
    # Application
    environment: str = "development"
    api_prefix: str = "/api"
    debug: bool = True
    
    @property
    def database_url_computed(self) -> str:
        # If DATABASE_URL is set directly, use it (for tests)
        if self.database_url:
            return self.database_url
        
        # Otherwise build from postgres variables (for development)
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()