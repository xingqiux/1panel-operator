from __future__ import annotations

from typing import Any, TypedDict


class HTTPResponseBody(TypedDict, total=False):
    text: str
    json: Any


class HTTPResponse(TypedDict):
    url: str
    status_code: int
    headers: dict[str, str]
    body: HTTPResponseBody


class ResponseMeta(TypedDict):
    status_code: int
    url: str


class NormalizedResponse(TypedDict, total=False):
    code: int
    message: str
    data: Any
    _meta: ResponseMeta


class PaginatedData(TypedDict, total=False):
    items: list[dict[str, Any]]
    total: int
