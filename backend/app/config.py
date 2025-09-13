# from pydantic_settings import BaseSettings

# class Settings(BaseSettings):
#     gemini_api_key: str
#     database_url: str
#     embedding_model: str = "gemini-embedding-001"
#     gen_model: str = "gemini-2.5-flash"
#     k_retrieval: int = 5

#     class Config:
#         env_file = ".env"
#         extra = "ignore"  # <--- add this line

# settings = Settings()