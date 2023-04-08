import httpx
import pytest

from open_ai import OpenaiClient

@pytest.fixture
def mock_post_response(httpx_mock):
    httpx_mock.add_response(
        method="POST",
        json={"data": [{"b64_json": "AAAYYYYYYLMAOOOO"}]}
    )

@pytest.fixture
def mock_post_response_fail(httpx_mock):
    httpx_mock.add_response(
        method="POST",
        status_code=400,
    )

@pytest.fixture
def mock_image_save(mocker):
    return mocker.patch("open_ai.client.OpenaiClient._save_jpg_from_b64")


@pytest.fixture
def client() -> OpenaiClient:
    return OpenaiClient(token="some-token-top-secret")

def test_correct_image_generation(client: OpenaiClient, mock_post_response, mock_image_save):
    result = client.generate_image_b64(definition="nice cat")

    assert result == "AAAYYYYYYLMAOOOO"
    mock_image_save.assert_not_called()

def test_correct_image_generation_with_save(client: OpenaiClient, mock_post_response, mock_image_save):
    result = client.generate_image_b64(definition="nice cat", save_jpg=True)

    assert result == "AAAYYYYYYLMAOOOO"
    mock_image_save.assert_called_once_with("AAAYYYYYYLMAOOOO")

def test_fail_image_generation_with_save(client: OpenaiClient, mock_post_response_fail):
    with pytest.raises(httpx.HTTPStatusError):
        client.generate_image_b64(definition="nice cat", save_jpg=True)