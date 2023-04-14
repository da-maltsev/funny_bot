import pytest

from bot.services import AskQuestionService


@pytest.fixture
def service(holiday_client, open_ai_client, context) -> AskQuestionService:
    return AskQuestionService(holiday_client=holiday_client, open_ai_client=open_ai_client, context=context)


@pytest.mark.parametrize(
    ("message", "ask_message", "toxic"),
    [
        ("Бот ответь Как твои дела?", "Как твои дела?", False),
        ("Как твои дела?", "Как твои дела?", False),
        ("Э слыш Как твои дела?", "Как твои дела?", True),
        ("Бот как думаешь Как твои дела?", "Как твои дела?", False),
        ("Слыш есть вопрос Как твои дела?", "Как твои дела?", True),
    ],
)
async def test_all_calls_were_made(service, mock_open_ai_call_ask, mock_send_message, message, ask_message, toxic):
    await service(chat_id=322, message=message)

    mock_open_ai_call_ask.assert_called_once_with(ask_message, toxic=toxic)
    mock_send_message.assert_called()
