from dataclasses import dataclass
from uuid import uuid4

from telegram.ext import ContextTypes

from clients.holiday.client import HolidayClient
from clients.open_ai.client import OpenaiClient


@dataclass
class BaseBotService:
    open_ai_client: OpenaiClient
    holiday_client: HolidayClient
    context: ContextTypes.DEFAULT_TYPE

    async def send_photo(self, chat_id: str | int, photo_name: str, description: str) -> None:
        await self.context.bot.send_photo(chat_id=chat_id, photo=photo_name)  # type: ignore
        await self.send_message(chat_id=chat_id, text=description)  # type: ignore

    async def send_message(self, chat_id: int | str, text: str):
        await self.context.bot.send_message(chat_id=chat_id, text=text)

    @classmethod
    def get_photo_name(cls) -> str:
        return f"{uuid4()}.jpg"
