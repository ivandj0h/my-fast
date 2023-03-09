# config.py
import os
from functools import lru_cache
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    env_name: str = "dev"
    redis_host: str = os.getenv("REDIS_HOST")
    redis_port: int = os.getenv("REDIS_PORT")
    redis_password: str = os.getenv("REDIS_PASSWORD")
    decode_responses: bool = os.getenv("DECODE_RESPONSES")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    settings = Settings()
    print(f"Loading Settings for : {settings.env_name}")
    return settings
