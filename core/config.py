from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GOOGLE_API_KEY:str
    MISTRAL_API_KEY:str
    HUGGING_FACE_API_KEY:str
    DATABASE_URL: str
    EMBEDDING_DIMENSION: int

    model_config=SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()