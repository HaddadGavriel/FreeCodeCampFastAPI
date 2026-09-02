from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    jwt_algorithm: str
    jwt_secret_key: str
    jwt_access_token_expire_minutes: int

    class Config:
        env_file = "app/.env"

settings = Settings()