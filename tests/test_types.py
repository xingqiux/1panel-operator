from __future__ import annotations

from onepanel.types import HTTPResponse, NormalizedResponse, PaginatedData


def test_http_response_type() -> None:
    response: HTTPResponse = {
        "url": "http://example.com",
        "status_code": 200,
        "headers": {"content-type": "application/json"},
        "body": {"text": "{}", "json": {}},
    }
    assert response["status_code"] == 200


def test_normalized_response_type() -> None:
    resp: NormalizedResponse = {
        "code": 200,
        "message": "success",
        "data": {"items": []},
    }
    assert resp["code"] == 200


def test_paginated_data_type() -> None:
    payload: PaginatedData = {
        "items": [{"id": 1}],
        "total": 1,
    }
    assert payload["total"] == 1
