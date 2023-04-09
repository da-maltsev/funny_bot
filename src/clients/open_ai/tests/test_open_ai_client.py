import pytest


@pytest.fixture
def mock_post_response_image(httpx_mock):
    httpx_mock.add_response(method="POST", json={"data": [{"b64_json": "AAAYYYYYYLMAOOOO"}]})


@pytest.fixture
def mock_post_response_chat(httpx_mock):
    httpx_mock.add_response(
        method="POST",
        json={
            "model": "gpt-3.5-turbo-0301",
            "usage": {
                "prompt_tokens": 30,
                "completion_tokens": 76,
                "total_tokens": 106,
            },
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "Как искусственный интеллект.",
                    },
                    "finish_reason": "stop",
                    "index": 0,
                }
            ],
        },
    )


@pytest.fixture
def mock_post_response_fail(httpx_mock):
    httpx_mock.add_response(
        method="POST",
        status_code=400,
    )


@pytest.fixture
def mock_image_save(mocker):
    return mocker.patch("clients.open_ai.client.OpenaiClient.save_jpg_from_b64")


@pytest.fixture
def mock_logger(mocker):
    return mocker.patch("logging.error")


async def test_correct_image_generation(open_ai_client, mock_post_response_image, mock_image_save, mock_logger):
    result = await open_ai_client.generate_image_b64(definition="nice cat")

    assert result == "AAAYYYYYYLMAOOOO"
    mock_image_save.assert_not_called()
    mock_logger.assert_not_called()


async def test_correct_image_generation_with_save(open_ai_client, mock_post_response_image, mock_image_save, mock_logger):
    result = await open_ai_client.generate_image_b64(definition="nice cat", filename="True")

    assert result == "AAAYYYYYYLMAOOOO"
    mock_image_save.assert_called_once_with("AAAYYYYYYLMAOOOO", "True")
    mock_logger.assert_not_called()


async def test_fail_image_generation(open_ai_client, mock_post_response_fail, mock_logger):
    await open_ai_client.generate_image_b64(definition="nice cat")

    mock_logger.assert_called_once()


async def test_success_answer_generation(open_ai_client, mock_post_response_chat, mock_logger):
    result = await open_ai_client.ask_chat_gpt("tell me why")

    mock_logger.assert_not_called()
    assert result == "Как искусственный интеллект."


async def test_fail_answer_generation(open_ai_client, mock_post_response_fail, mock_logger):
    result = await open_ai_client.ask_chat_gpt(message="nice cat")

    mock_logger.assert_called_once()
    assert result == open_ai_client.default_answer
