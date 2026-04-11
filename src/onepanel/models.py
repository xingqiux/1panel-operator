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
    def __init__(self, message: str, status_code: int | None = None, payload: Any = None):
        super().__init__(message)
        self.status_code = status_code
        self.payload = payload
