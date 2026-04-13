from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class ApiResult(BaseModel):
    ok: bool
    data: Any = None
    count: int | None = None
    meta: dict = {}
    error: str | None = None


class PanelAPIError(Exception):
    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        payload: Any = None,
        api_message: str | None = None,
        api_code: int | None = None,
    ):
        display_msg = api_message or message
        super().__init__(display_msg)
        self.message = message
        self.status_code = status_code
        self.payload = payload
        self.api_message = api_message
        self.api_code = api_code

    @property
    def hint(self) -> str | None:
        if self.status_code == 401:
            return "Check your API key in ONEPANEL_API_KEY"
        if self.status_code == 403:
            return "Permission denied. Verify API key permissions."
        if self.status_code == 404:
            return "Resource not found. Check the endpoint path."
        if self.status_code and self.status_code >= 500:
            return "Server error. Try again later or check 1Panel logs."
        return None
