import pytest


@pytest.fixture
def context(mocker):
    context = mocker.patch("telegram.ext.ContextTypes", autospec=True)
    return context.return_value


@pytest.fixture
def mock_open_ai_call(mocker):
    return mocker.patch("clients.open_ai.client.OpenaiClient.generate_image_b64", return_value=None)


@pytest.fixture
def mock_open_ai_call_ask(mocker):
    return mocker.patch("clients.open_ai.client.OpenaiClient.ask_chat_gpt", return_value=None)


@pytest.fixture
def mock_photo_name(mocker):
    return mocker.patch("bot.services.base_bot_service.BaseBotService.get_photo_name", return_value="lmao.jpg")


@pytest.fixture
def mock_send_photo(mocker):
    return mocker.patch("bot.services.base_bot_service.BaseBotService.send_photo", return_value=None)


@pytest.fixture
def mock_send_message(mocker):
    return mocker.patch("bot.services.base_bot_service.BaseBotService.send_message", return_value=None)


@pytest.fixture
def mock_remove_file(mocker):
    return mocker.patch("os.remove", return_value=None)
