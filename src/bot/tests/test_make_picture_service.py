import pytest

from bot.services import PictureMaker


@pytest.fixture
def service(holiday_client, open_ai_client, context) -> PictureMaker:
    return PictureMaker(holiday_client=holiday_client, open_ai_client=open_ai_client, context=context)


async def test_all_calls_were_made(service, mocker, mock_open_ai_call, mock_photo_name, mock_remove_file, mock_send_photo, mock_send_message):
    await service(chat_id=322, description="doge")

    mock_open_ai_call.assert_called_once_with("doge", filename="lmao.jpg")
    mock_send_photo.assert_called_once_with(322, "lmao.jpg", 'Это вот "doge"')
    mock_photo_name.assert_called_once()
    mock_remove_file.assert_called_once_with("lmao.jpg")
    mock_send_message.assert_called()
