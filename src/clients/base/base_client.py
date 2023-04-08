from dataclasses import dataclass
import logging

import httpx


@dataclass
class BaseClient:
    token: str

    @classmethod
    def _check_response(cls, response: httpx.Response) -> None:
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            logging.error(e)
