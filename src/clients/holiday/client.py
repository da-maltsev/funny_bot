from dataclasses import dataclass
import datetime
from json import JSONDecodeError
from typing import Optional
from urllib.parse import urljoin

import httpx

from clients import BaseClient


@dataclass
class HolidayClient(BaseClient):
    base_url: str = "https://holidayapi.com/v1/"

    true_holiday: str = "Nice person birthday"

    def __post_init__(self):
        self.headers = {"Content-Type": "application/json"}
        self.params = {"key": self.token}

    async def get_list_of_holidays(
        self,
        month: int,
        year: int,
        day: Optional[int] = None,
        country: str = "RU",
    ) -> list:
        params = {
            "day": day,
            "month": month,
            "year": year,
            "country": country,
        }
        params.update(self.params)
        params = {k: v for k, v in params.items() if v}

        async with httpx.AsyncClient() as session:
            response = await session.get(
                urljoin(self.base_url, "holidays"),
                headers=self.headers,
                params=params,  # type: ignore
                timeout=10,
            )
        self._check_response(response)

        return self._get_list_of_holidays_from_response(response)

    @classmethod
    def _get_list_of_holidays_from_response(cls, response: httpx.Response) -> list[tuple[str, datetime.date]]:
        anyway_result = [(cls.true_holiday, datetime.date(1999, 9, 9))]

        try:
            content = response.json()
        except JSONDecodeError:
            return anyway_result

        raw_holidays = content.get("holidays")
        if not raw_holidays or len(raw_holidays) == 0:
            raw_holidays = [{True: True}]

        holidays = [
            (
                item.get("name", cls.true_holiday),
                datetime.datetime.strptime(item.get("date", "1999-09-09"), "%Y-%m-%d").date(),
            )
            for item in raw_holidays
        ]
        return holidays
