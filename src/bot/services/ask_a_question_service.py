from random import choice
from typing import Optional

from bot.filters import ask_question_filter
from bot.services.base_bot_service import BaseBotService


class AskQuestionService(BaseBotService):
    let_me_think: list[str] = [
        "Надо подумать...",
        "Надо покумекать...",
        "Ну-ка паддажи...",
        "Так так так...",
        "Дайте минутку...",
        "Отвечает Никита...",
        "Сейчас отвечу. Также рекомендую попробовать продолжить общение в веб-версии по адресу https://urf4cknmt.space . Там сохраняется контекст предыдущих сообщений и вообще там круто",
    ]

    async def __call__(self, chat_id: int, message: Optional[str], user_name: Optional[str] = None) -> None:
        if not message:
            return None

        len_of_trigger = ask_question_filter.len_trigger(message)
        toxic = ask_question_filter.is_toxic(message)
        message = message[len_of_trigger::]

        wait_text = choice(self.let_me_think)
        await self.send_message(chat_id, wait_text)

        try:
            text = await self.open_ai_client.ask_chat_gpt(message, toxic=toxic)
        except Exception:
            text = "что-то пошло не так, дорогой друг"

        response = f"{self.get_autoresponse(user_name).title()}, вот что я скажу:\n{text}"
        await self.send_message(chat_id, response)
