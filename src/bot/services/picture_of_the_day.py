from collections import namedtuple
import datetime
import os
from uuid import uuid4

from anyday_holiday import PictureDescriptorGenerator
from bot.services import BaseBotService


class PictureOfTheDay(BaseBotService):
    picture_descriptor_generator: PictureDescriptorGenerator = PictureDescriptorGenerator()

    async def __call__(self, chat_id: int) -> None:
        [description, text] = await self.get_picture_description_for_today()
        photo_name = f"{uuid4()}.jpg"

        await self.open_ai_client.generate_image_b64(description, filename=photo_name)
        await self.context.bot.send_photo(chat_id=chat_id, photo=photo_name)  # type: ignore
        await self.context.bot.send_message(chat_id=chat_id, text=f'This is "{text}"')  # type: ignore

        os.remove(photo_name)

    async def get_picture_description_for_today(self) -> tuple[str, str]:
        today = self._get_today_for_holiday()
        holidays = await self.holiday_client.get_list_of_holidays(day=today.day, month=today.month, year=today.year)
        holiday = holidays[0][0]
        text = holiday

        if holiday == self.holiday_client.true_holiday:
            holiday = self.picture_descriptor_generator()

        return holiday, text

    @classmethod
    def _get_today_for_holiday(cls):
        [day, month, year] = datetime.datetime.now().strftime("%d,%m,%Y").split(",")
        year = int(year) - 1

        Today = namedtuple("Today", "day month year")
        return Today(int(day), int(month), year)
