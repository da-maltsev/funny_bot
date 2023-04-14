import pytest

from bot.services.base_bot_service import BaseBotService


@pytest.fixture
def service(open_ai_client, context) -> BaseBotService:
    return BaseBotService(open_ai_client=open_ai_client, context=context)


def test_get_photo_name(mocker, service):
    mock_uuid = mocker.patch("bot.services.base_bot_service.uuid4", return_value="test-str")

    result = service.get_photo_name()

    assert result == "test-str.jpg"
    mock_uuid.assert_called_once()


@pytest.mark.parametrize(
    ("user_name", "response"),
    [
        ("doge", "doge"),
        (None, "дружище"),
    ],
)
def test_get_autoresponse(service, user_name, response):
    result = service.get_autoresponse(user_name)

    assert result == response
