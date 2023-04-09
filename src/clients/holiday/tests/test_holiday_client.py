import datetime
import pytest


@pytest.fixture
def holidays():
    return [
        {
            "name": "Easter",
            "date": "2022-04-17",
            "observed": "2022-04-17",
            "public": False,
            "country": "RU",
            "uuid": "cad13d0b-4e76-4539-91f9-c538ae08fcd1",
            "weekday": {"date": {"name": "Sunday", "numeric": "7"}, "observed": {"name": "Sunday", "numeric": "7"}},
        },
        {
            "name": "Local Self-Government Day",
            "date": "2022-04-21",
            "country": "RU",
            "uuid": "7f9fb033-9fc3-470a-b396-17442a78497d",
        },
    ]


@pytest.fixture
def mock_get_response(httpx_mock, holidays):
    httpx_mock.add_response(
        method="GET",
        json={
            "status": 200,
            "requests": {"used": 13, "available": 9987, "resets": "2023-05-01 00:00:00"},
            "holidays": holidays,
        },
    )


@pytest.fixture
def mock_get_response_no_holidays(httpx_mock):
    httpx_mock.add_response(
        method="GET",
        json={
            "status": 200,
            "requests": {"used": 13, "available": 9987, "resets": "2023-05-01 00:00:00"},
            "holidays": [],
        },
    )


@pytest.fixture
def mock_get_response_fail(httpx_mock):
    httpx_mock.add_response(
        method="GET",
        status_code=400,
    )


@pytest.fixture
def result_list():
    return [("Easter", datetime.date(2022, 4, 17)), ("Local Self-Government Day", datetime.date(2022, 4, 21))]


@pytest.fixture
def mock_logger(mocker):
    return mocker.patch("logging.error")


async def test_succeess_get_holidays(holiday_client, result_list, mock_get_response, mock_logger):
    result = await holiday_client.get_list_of_holidays(4, 4, 2022)

    assert result == result_list
    mock_logger.assert_not_called()


async def test_succeess_get_holidays_of_empty_list(holiday_client, mock_get_response_no_holidays, mock_logger):
    result = await holiday_client.get_list_of_holidays(4, 4, 2022)

    assert result == [(holiday_client.true_holiday, datetime.date(1999, 9, 9))]
    mock_logger.assert_not_called()


async def test_fail_get_holidays(holiday_client, mock_get_response_fail, mock_logger):
    await holiday_client.get_list_of_holidays(4, 4, 2022)

    mock_logger.assert_called_once()
