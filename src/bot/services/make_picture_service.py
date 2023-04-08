import os
from typing import Optional
from uuid import uuid4

from bot.services import BaseBotService


class PictureMaker(BaseBotService):
    async def __call__(self, chat_id: int, description: Optional[str]) -> None:
        if not description:
            return None

        photo_name = f"{uuid4()}.jpg"

        await self.open_ai_client.generate_image_b64(description, filename=photo_name)
        await self.context.bot.send_photo(chat_id=chat_id, photo=photo_name)  # type: ignore
        await self.context.bot.send_message(chat_id=chat_id, text=f'Это вот "{description}"')  # type: ignore

        os.remove(photo_name)
