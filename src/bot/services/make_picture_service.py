import os
from typing import Optional

from bot.filters import make_picture_filter
from bot.services.base_bot_service import BaseBotService


class PictureMaker(BaseBotService):
    async def __call__(self, chat_id: int, description: Optional[str]) -> None:
        len_of_trigger = make_picture_filter.len_trigger(description)  # type: ignore
        description = description[len_of_trigger::]  # type: ignore

        if not description:
            return None

        photo_name = self.get_photo_name()
        await self.open_ai_client.generate_image_b64(description, filename=photo_name)

        description = self.make_description(description)
        await self.send_photo(chat_id, photo_name, description)

        os.remove(photo_name)

    @classmethod
    def make_description(cls, description: str) -> str:
        return f'Это вот "{description}"'
