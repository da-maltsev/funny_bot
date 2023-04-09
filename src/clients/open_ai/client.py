import base64
from dataclasses import dataclass
from json import JSONDecodeError
from typing import Optional
from urllib.parse import urljoin

import httpx

from clients import BaseClient


@dataclass
class OpenaiClient(BaseClient):
    base_url: str = "https://api.openai.com/v1/"
    image_name: str = "temp_image.jpg"

    timeout: float = 60.0
    default_answer: str = "Нейросеть не в силах вам помочь"

    def __post_init__(self) -> None:
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    async def generate_image_b64(self, definition: str, size: str = "512x512", filename: Optional[str] = None) -> Optional[str]:
        data = {
            "prompt": definition,
            "n": 1,
            "size": size,
            "response_format": "b64_json",
        }

        async with httpx.AsyncClient() as session:
            response = await session.post(
                url=urljoin(self.base_url, "images/generations"),
                headers=self.headers,
                json=data,
                timeout=self.timeout / 2,
            )
        self._check_response(response)

        b64_content = self._get_b64_content(response)

        if filename and b64_content:
            self.save_jpg_from_b64(b64_content, filename)

        return b64_content

    async def ask_chat_gpt(self, message: str, toxic: bool = False) -> str:
        message = message if not toxic else f"{message} Ответь так, как будто ты хулиган и хочешь быть высокомерным."
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": message,
                },
            ],
            "temperature": 0.5,
        }

        async with httpx.AsyncClient() as session:
            response = await session.post(
                url=urljoin(self.base_url, "chat/completions"),
                headers=self.headers,
                json=data,
                timeout=self.timeout,
            )
        self._check_response(response)

        return self.get_answer_from_response(response)

    @classmethod
    def _get_json_content(cls, response: httpx.Response):
        try:
            return response.json()
        except JSONDecodeError:
            return None

    @classmethod
    def save_jpg_from_b64(cls, b64_string: str, filename: str = "temp_image.jpg") -> None:
        imgdata = base64.b64decode(b64_string)
        with open(filename, "wb") as f:
            f.write(imgdata)

    @classmethod
    def _get_b64_content(cls, response: httpx.Response) -> Optional[str]:
        content = cls._get_json_content(response)
        b64_content = None
        try:
            b64_content = content.get("data")[False].get("b64_json")  # ayyy lmao False index
        finally:
            return b64_content

    @classmethod
    def get_answer_from_response(cls, response: httpx.Response) -> str:
        content = cls._get_json_content(response)
        if not content:
            return cls.default_answer

        answer = cls.default_answer
        try:
            first_choice = content.get("choices")[0]
            message = first_choice.get("message")
            answer = message.get("content", cls.default_answer)
        finally:
            return answer
