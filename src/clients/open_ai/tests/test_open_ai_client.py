import pytest

from clients import OpenaiClient


@pytest.fixture
def mock_post_response(httpx_mock):
    httpx_mock.add_response(method="POST", json={"data": [{"b64_json": "AAAYYYYYYLMAOOOO"}]})


@pytest.fixture
def mock_post_response_fail(httpx_mock):
    httpx_mock.add_response(
        method="POST",
        status_code=400,
    )


@pytest.fixture
def mock_image_save(mocker):
    return mocker.patch("clients.open_ai.client.OpenaiClient._save_jpg_from_b64")


@pytest.fixture
def client() -> OpenaiClient:
    return OpenaiClient(token="some-token-top-secret")


@pytest.fixture
def mock_logger(mocker):
    return mocker.patch("logging.error")


def test_correct_image_generation(client: OpenaiClient, mock_post_response, mock_image_save, mock_logger):
    result = client.generate_image_b64(definition="nice cat")

    assert result == "AAAYYYYYYLMAOOOO"
    mock_image_save.assert_not_called()
    mock_logger.assert_not_called()


def test_correct_image_generation_with_save(client: OpenaiClient, mock_post_response, mock_image_save, mock_logger):
    result = client.generate_image_b64(definition="nice cat", save_jpg=True)

    assert result == "AAAYYYYYYLMAOOOO"
    mock_image_save.assert_called_once_with("AAAYYYYYYLMAOOOO")
    mock_logger.assert_not_called()


def test_fail_image_generation(client: OpenaiClient, mock_post_response_fail, mock_logger):
    client.generate_image_b64(definition="nice cat")

    mock_logger.assert_called_once()
