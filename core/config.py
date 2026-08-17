from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    API_URL: str
    UPLOAD_DIR: str

    # Google OAuth2
    GOOGLE_CLIENT_ID: str

    # JWT propio
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()