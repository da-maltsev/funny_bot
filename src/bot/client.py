from dataclasses import dataclass
import logging
from typing import Callable

from telegram import Update
from telegram.ext import ApplicationBuilder
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes
from telegram.ext import filters
from telegram.ext import MessageHandler

from bot.filters import make_picture_filter
from bot.services import PictureMaker
from bot.services import PictureOfTheDay
from clients.holiday.client import HolidayClient
from clients.open_ai.client import OpenaiClient

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)


@dataclass
class TelegramBot:
    token: str
    open_ai_client: OpenaiClient
    holiday_client: HolidayClient

    def __post_init__(self):
        self.application = ApplicationBuilder().token(self.token).build()
        self.clients = [self.open_ai_client, self.holiday_client]

    def __call__(self):
        self.add_handlers()
        self.application.run_polling()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        logging.warn("Someone started")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Здарова!\nЯ полезный ботяра, чтобы узнать, что я могу, введи /help")  # type: ignore

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,  # type: ignore
            text="\nКоманда /make_picture просит нейросеть сделать картинку с твоим описанием\
                                       \nКоманда /today_picture узнает, есть ли сегодня праздник и пришлёт иллюстарцию к нему, если праздника нет, то пришлёт просто что-то приятное.",
        )

    async def today_picture(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        logging.info("aaaaa today")
        await PictureOfTheDay(*self.clients, context)(update.effective_chat.id)  # type: ignore

    async def make_picture_by_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        text = update.message.text  # type: ignore
        len_of_trigger = make_picture_filter.len_trigger(text)  # type: ignore
        description = text[len_of_trigger::]  # type: ignore
        logging.info(description)

        await PictureMaker(*self.clients, context)(update.effective_chat.id, description)  # type: ignore

    def add_handlers(self) -> None:
        self.add_commands(
            [
                self.start,
                self.help,
                self.today_picture,
            ]
        )
        self.add_message_nadlers()

    def add_commands(self, functions: list[Callable]) -> None:
        for func in functions:
            self.application.add_handler(CommandHandler(func.__name__, func))

    def add_message_nadlers(self) -> None:
        self.application.add_handler(MessageHandler(make_picture_filter & (~filters.COMMAND), self.make_picture_by_message))
