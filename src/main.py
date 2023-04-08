from bot import TelegramBot
from clients import HolidayClient
from clients import OpenaiClient
from settings import settings

if __name__ == "__main__":
    open_ai_client = OpenaiClient(settings.OPENAI_TOKEN)
    holiday_client = HolidayClient(settings.HOLIDAY_TOKEN)
    telegram_bot = TelegramBot(
        token=settings.TELEGRAM_TOKEN,
        open_ai_client=open_ai_client,
        holiday_client=holiday_client,
    )

    telegram_bot()
