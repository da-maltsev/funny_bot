import pytest

from bot.services import PictureMaker


@pytest.fixture
def service(open_ai_client, context) -> PictureMaker:
    return PictureMaker(open_ai_client=open_ai_client, context=context)


@pytest.mark.parametrize(
    ("description", "photo_description", "user_name"),
    [
        ("doge", 'Дружище, это вот "doge"', None),
        ("doge", 'Никита, это вот "doge"', "никита"),
        ("doge", 'John, это вот "doge"', "John"),
        ("doge", 'Wysiwyg, это вот "doge"', "wysiwyg"),
    ],
)
async def test_all_calls_were_made(
    service, description, photo_description, user_name, mock_open_ai_call, mock_photo_name, mock_remove_file, mock_send_photo, mock_send_message
):
    await service(chat_id=322, description=description, user_name=user_name)

    mock_open_ai_call.assert_called_once_with(description, filename="lmao.jpg")
    mock_send_photo.assert_called_once_with(322, "lmao.jpg", photo_description)
    mock_photo_name.assert_called_once()
    mock_remove_file.assert_called_once_with("lmao.jpg")
    mock_send_message.assert_called()
