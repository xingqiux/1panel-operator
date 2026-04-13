from __future__ import annotations

import pytest
from pytest_httpx import HTTPXMock

from onepanel.client import PanelClient
from onepanel.config import PanelConfig
from onepanel.models import PanelAPIError


@pytest.fixture
def config(monkeypatch):
    monkeypatch.setenv("ONEPANEL_BASE_URL", "http://test-panel:8080")
    monkeypatch.setenv("ONEPANEL_API_KEY", "test-key-1234567890")
    return PanelConfig()


@pytest.fixture
def client(config):
    return PanelClient(config)


def test_request_injects_auth_headers(client: PanelClient, httpx_mock: HTTPXMock):
    body = {"code": 200, "message": "success", "data": []}
    httpx_mock.add_response(json=body)
    client.request("GET", "/websites/list")
    request = httpx_mock.get_request()
    assert "1Panel-Token" in request.headers
    assert "1Panel-Timestamp" in request.headers


def test_request_get_success(client: PanelClient, httpx_mock: HTTPXMock):
    body = {"code": 200, "message": "success", "data": {"items": []}}
    httpx_mock.add_response(json=body)
    result = client.request("GET", "/apps/installed/list")
    assert result["status_code"] == 200
    assert result["body"]["json"] == body


def test_request_http_error_raises_panel_api_error(client: PanelClient, httpx_mock: HTTPXMock):
    httpx_mock.add_response(status_code=500, json={"code": 500, "message": "internal error"})
    with pytest.raises(PanelAPIError) as exc_info:
        client.request("GET", "/bad-endpoint")
    exc = exc_info.value
    assert exc.status_code == 500
    assert exc.api_message == "internal error"
    assert exc.api_code == 500
    assert str(exc) == "internal error"
    assert exc.hint == "Server error. Try again later or check 1Panel logs."


def test_ping(client: PanelClient, httpx_mock: HTTPXMock):
    body = {"code": 200, "message": "success", "data": []}
    httpx_mock.add_response(json=body)
    result = client.ping()
    request = httpx_mock.get_request()
    assert "/api/v1/websites/list" in str(request.url)
    assert result["status_code"] == 200


def test_plan_safe_method(client: PanelClient):
    plan = client.plan("GET", "/websites/list")
    assert plan["write_operation"] is False
    assert plan["method"] == "GET"


def test_plan_write_method(client: PanelClient):
    plan = client.plan("POST", "/websites/update", body={"id": 1})
    assert plan["write_operation"] is True
    assert plan["method"] == "POST"
    assert plan["body"] == {"id": 1}


def test_normalize_response_1panel_envelope(client: PanelClient):
    response = {
        "url": "http://test-panel:8080/api/v1/test",
        "status_code": 200,
        "headers": {},
        "body": {
            "text": "...",
            "json": {"code": 200, "message": "success", "data": {"key": "value"}},
        },
    }
    normalized = client.normalize_response_payload(response)
    assert normalized["code"] == 200
    assert normalized["message"] == "success"
    assert normalized["data"] == {"key": "value"}
    assert "_meta" in normalized


def test_normalize_response_non_envelope(client: PanelClient):
    response = {
        "url": "http://test-panel:8080/api/v1/test",
        "status_code": 200,
        "headers": {},
        "body": {
            "text": "plain text",
        },
    }
    normalized = client.normalize_response_payload(response)
    assert normalized["data"] == "plain text"
    assert "_meta" in normalized
