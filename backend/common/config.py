from pydantic_settings import BaseSettings, SettingsConfigDict # type: ignore

class Settings(BaseSettings):
    openai_api_key: str = ""
    openweather_api_key: str = ""
    telegram_bot_token: str = ""
    gen_model: str = "gpt-4o-mini"
    embedding_model: str = "text-embedding-3-small"
    embed_dim: int = 1536
    database_url: str = ""
    k_retrieval: int = 5
    
    allowed_file_types: list = [".pdf"]

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()
