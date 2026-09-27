from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GOOGLE_API_KEY:str
    MISTRAL_API_KEY:str
    HUGGING_FACE_API_KEY:str

    model_config=SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()