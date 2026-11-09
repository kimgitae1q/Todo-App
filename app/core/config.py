import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL", "")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "").split(",")


@dataclass(frozen=True)
class Settings:
    database_url: str
    cors_origins: list[str]


def get_settings() -> Settings:
    return Settings(database_url=DB_URL, cors_origins=CORS_ORIGINS)
