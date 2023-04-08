from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    OPENAI_TOKEN: str = getenv("OPENAI_TOKEN", "top-secret")
    HOLIDAY_TOKEN: str = getenv("HOLIDAY_TOKEN", "top-secret")
    TELEGRAM_TOKEN: str = getenv("TELEGRAM_TOKEN", "top-secret")


settings = Settings()
