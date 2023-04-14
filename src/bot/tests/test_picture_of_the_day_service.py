import datetime
import pytest

from bot.services.picture_of_the_day import PictureOfTheDay


@pytest.fixture
def mock_picture_descriptor(mocker):
    mocker.patch("anyday_holiday.picture_descriptor.PictureDescriptorGenerator.__call__", return_value="something")


@pytest.fixture
def service(holiday_client, open_ai_client, context, mock_picture_descriptor) -> PictureOfTheDay:
    return PictureOfTheDay(holiday_client=holiday_client, open_ai_client=open_ai_client, context=context)


async def test_all_calls_were_made(service, mocker, mock_open_ai_call, mock_photo_name, mock_remove_file, mock_send_photo, mock_send_message):
    mock_get_holiday = mocker.patch(
        "clients.holiday.client.HolidayClient.get_list_of_holidays",
        return_value=[
            (
                "Friday",
                datetime.date(2023, 4, 4),
            )
        ],
    )

    await service(322)

    mock_get_holiday.assert_called_once()
    mock_open_ai_call.assert_called_once_with("Friday", filename="lmao.jpg")
    mock_remove_file.assert_called_once_with("lmao.jpg")
    mock_send_photo.assert_called_once_with(322, "lmao.jpg", description="Friday")
    mock_send_message.assert_called()


async def test_all_calls_were_made_no_holiday(service, mocker, mock_open_ai_call, mock_photo_name, mock_remove_file, mock_send_photo, mock_send_message):
    mock_get_holiday = mocker.patch(
        "clients.holiday.client.HolidayClient.get_list_of_holidays",
        return_value=[
            (
                service.holiday_client.true_holiday,
                datetime.date(2023, 9, 9),
            )
        ],
    )

    await service(322)

    mock_get_holiday.assert_called_once()
    mock_open_ai_call.assert_called_once_with("something", filename="lmao.jpg")
    mock_remove_file.assert_called_once_with("lmao.jpg")
    mock_send_photo.assert_called_once_with(322, "lmao.jpg", description=f"Не забывайте никогда о том, что 09/09 {service.holiday_client.true_holiday}")
    mock_send_message.assert_called()
