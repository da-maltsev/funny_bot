import pytest

from clients import HolidayClient
from clients import OpenaiClient


@pytest.fixture
def open_ai_client() -> OpenaiClient:
    return OpenaiClient(token="some-token-top-secret")


@pytest.fixture
def holiday_client() -> HolidayClient:
    return HolidayClient(token="top-secret-token")
