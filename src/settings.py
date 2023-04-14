from dataclasses import dataclass
from os import getenv
from typing import Optional

from dotenv import load_dotenv
import sentry_sdk

load_dotenv()


@dataclass
class Settings:
    OPENAI_TOKEN: str = getenv("OPENAI_TOKEN", "top-secret")
    TELEGRAM_TOKEN: str = getenv("TELEGRAM_TOKEN", "top-secret")
    SENTRY_DSN: Optional[str] = getenv("SENTRY_DSN", None)


settings = Settings()

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    traces_sample_rate=0.5,
)
