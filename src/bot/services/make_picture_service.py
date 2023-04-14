import os
from typing import Optional

from bot.filters import make_picture_filter
from bot.services.base_bot_service import BaseBotService


class PictureMaker(BaseBotService):
    async def __call__(self, chat_id: int, description: Optional[str], user_name: Optional[str] = None) -> None:
        len_of_trigger = make_picture_filter.len_trigger(description)  # type: ignore
        description = description[len_of_trigger::]  # type: ignore

        if not description:
            return None

        await self.send_message(chat_id, text=f"Сейчас собразим что это такое - {description}")

        photo_uuid = self.get_photo_name()
        await self.open_ai_client.generate_image_b64(description, filename=photo_uuid)

        description = self.make_description(description, user_name)
        await self.send_photo(chat_id, photo_uuid, description)

        os.remove(photo_uuid)

    @classmethod
    def make_description(cls, description: str, user_name: Optional[str]) -> str:
        return f'{cls.get_autoresponse(user_name).title()}, это вот "{description}"'
