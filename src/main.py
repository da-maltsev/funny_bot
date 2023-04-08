from holiday.client import HolidayClient
from open_ai.client import OpenaiClient
from settings import settings

open_ai_client = OpenaiClient(settings.OPENAI_TOKEN)
holiday_client = HolidayClient(settings.HOLIDAY_TOKEN)
