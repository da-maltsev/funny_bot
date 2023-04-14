from dataclasses import dataclass
import logging
from typing import Callable

from telegram import Update
from telegram.ext import ApplicationBuilder
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes
from telegram.ext import filters
from telegram.ext import MessageHandler

from bot.filters import ask_question_filter
from bot.filters import make_picture_filter
from bot.help_text import help_text
from bot.services import AskQuestionService
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
        await context.bot.send_message(chat_id=update.effective_chat.id, text=help_text.get("start", "Hello there!"))  # type: ignore

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,  # type: ignore
            text=help_text.get("help", "Just figure it out bro"),
        )

    async def today_picture(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        logging.info("today picture was called")
        await PictureOfTheDay(*self.clients, context)(update.effective_chat.id)  # type: ignore

    async def make_picture(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        logging.info(update.message.text)  # type: ignore
        await PictureMaker(*self.clients, context)(update.effective_chat.id, update.message.text)  # type: ignore

    async def ask_question(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        logging.info(update.message.text)  # type: ignore
        await AskQuestionService(*self.clients, context)(update.effective_chat.id, update.message.text)  # type: ignore

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
        self.application.add_handler(MessageHandler(make_picture_filter & (~filters.COMMAND), self.make_picture))
        self.application.add_handler(MessageHandler(ask_question_filter & (~filters.COMMAND), self.ask_question))
