from __future__ import annotations

import json

from typer.testing import CliRunner

runner = CliRunner()


def test_ping_reports_api_error_hint(httpx_mock):
    from onepanel.cli import app as root_app

    httpx_mock.add_response(
        status_code=401,
        json={"code": 401, "message": "invalid api key"},
    )

    result = runner.invoke(
        root_app,
        ["ping"],
        env={
            "ONEPANEL_BASE_URL": "http://test-panel:8080",
            "ONEPANEL_API_KEY": "test-key-1234567890",
        },
    )

    assert result.exit_code == 1
    assert json.loads(result.output) == {
        "api_message": "invalid api key",
        "error": "invalid api key",
        "hint": "Check your API key in ONEPANEL_API_KEY",
        "ok": False,
        "status_code": 401,
    }
