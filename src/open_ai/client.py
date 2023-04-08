import base64
from dataclasses import dataclass
from json import JSONDecodeError
from typing import Optional
from urllib.parse import urljoin

import httpx

from base import BaseClient


@dataclass
class OpenaiClient(BaseClient):
    base_url: str = "https://api.openai.com/v1/"

    def __post_init__(self) -> None:
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def generate_image_b64(self, definition: str, size: str = "1024x1024", save_jpg: bool = False) -> Optional[str]:
        data = {
            "prompt": definition,
            "n": 1,
            "size": size,
            "response_format": "b64_json",
        }

        response = httpx.post(
            url=urljoin(self.base_url, "images/generations"),
            headers=self.headers,
            json=data,
            timeout=10,
        )
        self._check_response(response)

        b64_content = self._get_b64_content(response)

        if save_jpg and b64_content:
            self._save_jpg_from_b64(b64_content)

        return b64_content

    @classmethod
    def _save_jpg_from_b64(cls, b64_string: str, filename: str = "today_image.jpg") -> None:
        imgdata = base64.b64decode(b64_string)
        with open(filename, "wb") as f:
            f.write(imgdata)

    @classmethod
    def _get_b64_content(cls, response: httpx.Response) -> Optional[str]:
        try:
            content = response.json()
        except JSONDecodeError:
            return None

        b64_content = None
        try:
            b64_content = content.get("data")[False].get("b64_json")  # ayyy lmao False index
        finally:
            return b64_content
