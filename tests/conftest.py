from __future__ import annotations

import pytest

from onepanel.config import PanelConfig


@pytest.fixture
def mock_config(monkeypatch):
    monkeypatch.setenv("ONEPANEL_BASE_URL", "http://test-panel:8080")
    monkeypatch.setenv("ONEPANEL_API_KEY", "test-key-1234567890")
    return PanelConfig()


@pytest.fixture
def sample_1panel_response():
    """Standard 1Panel API success response envelope."""
    return {
        "url": "http://test-panel:8080/api/v1/test",
        "status_code": 200,
        "headers": {"content-type": "application/json"},
        "body": {
            "text": '{"code":200,"message":"success","data":{}}',
            "json": {"code": 200, "message": "success", "data": {}},
        },
    }
