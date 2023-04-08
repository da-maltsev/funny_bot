from dataclasses import dataclass

from telegram.ext import ContextTypes

from clients.holiday.client import HolidayClient
from clients.open_ai.client import OpenaiClient


@dataclass
class BaseBotService:
    open_ai_client: OpenaiClient
    holiday_client: HolidayClient
    context: ContextTypes.DEFAULT_TYPE
