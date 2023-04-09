from collections import namedtuple
import pytest

from bot.filters import make_picture_filter


@pytest.fixture
def filter():
    return make_picture_filter


@pytest.mark.parametrize(
    ("start_phrase", "is_true"),
    [
        ("Картинка, где", True),
        ("Картинка где", True),
        ("Бот дай картинку, где", True),
        ("Бот дай картинку где", True),
        ("Хочу картинку где", True),
        ("Хочу картинку, где", True),
        ("Это не работает", False),
    ],
)
def test_filter_passes_correct_phrase(filter, start_phrase, is_true):
    phrase = f"{start_phrase} мужик в шляпе и она ему как раз"
    message = namedtuple("message", "text")

    result = filter.filter(message(phrase))

    assert result is is_true


@pytest.mark.parametrize(
    "start_phrase",
    [
        "Картинка, где",
        "Картинка где",
        "Бот дай картинку, где",
        "Бот дай картинку где",
        "Хочу картинку где",
        "Хочу картинку, где",
    ],
)
def test_filter_finds_correct_len(filter, start_phrase):
    phrase = f"{start_phrase} мужик в шляпе и она ему как раз"
    len_phrase = len(start_phrase) + 1  # space symbol

    result = filter.len_trigger(phrase)

    assert result == len_phrase
