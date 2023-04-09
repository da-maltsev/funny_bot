import os
from typing import Optional

from bot.services import BaseBotService


class PictureMaker(BaseBotService):
    async def __call__(self, chat_id: int, description: Optional[str]) -> None:
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
