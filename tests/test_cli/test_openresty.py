from __future__ import annotations

import json

from typer.testing import CliRunner

runner = CliRunner()


def _make_fake_client(normalized):
    class FakeClient:
        def __init__(self) -> None:
            self.requests: list[tuple[str, str, object, object, object]] = []

        def request(self, method, path, body=None, query=None, extra_headers=None):
            self.requests.append((method, path, body, query, extra_headers))
            return {"ok": True}

        def normalize_response_payload(self, response):
            return normalized

    return FakeClient()


def test_openresty_help():
    from onepanel.cli.openresty import app

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    output = result.output.lower()
    assert "status" in output
    assert "config" in output


def test_root_help_includes_openresty_subcommand():
    from onepanel.cli import app as root_app

    result = runner.invoke(root_app, ["--help"])
    assert result.exit_code == 0
    assert "openresty" in result.output.lower()


def test_openresty_status_help():
    from onepanel.cli.openresty import app

    result = runner.invoke(app, ["status", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output


def test_openresty_config_help():
    from onepanel.cli.openresty import app

    result = runner.invoke(app, ["config", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output


def test_openresty_status(monkeypatch):
    from onepanel.cli import openresty

    fake_client = _make_fake_client(
        {
            "data": {
                "connections": 123,
                "accepts": 456,
                "handled": 456,
                "requests": 789,
                "reading": 1,
                "writing": 2,
                "waiting": 3,
            }
        }
    )
    monkeypatch.setattr(openresty, "get_client", lambda ctx: fake_client)

    result = runner.invoke(openresty.app, ["status"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("GET", "/openresty", None, None, None),
    ]
    assert json.loads(result.output) == {
        "connections": 123,
        "accepts": 456,
        "handled": 456,
        "requests": 789,
        "reading": 1,
        "writing": 2,
        "waiting": 3,
    }


def test_openresty_status_raw(monkeypatch):
    from onepanel.cli import openresty

    normalized = {
        "data": {
            "connections": 11,
            "accepts": 22,
            "handled": 22,
            "requests": 33,
            "reading": 4,
            "writing": 5,
            "waiting": 6,
        },
        "_meta": {"status_code": 200, "url": "http://test-panel/api/v1/openresty"},
    }
    fake_client = _make_fake_client(normalized)
    monkeypatch.setattr(openresty, "get_client", lambda ctx: fake_client)

    result = runner.invoke(openresty.app, ["status", "--raw"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("GET", "/openresty", None, None, None),
    ]
    assert json.loads(result.output) == normalized


def test_openresty_config(monkeypatch):
    from onepanel.cli import openresty

    fake_client = _make_fake_client({"data": "worker_processes auto;"})
    monkeypatch.setattr(openresty, "get_client", lambda ctx: fake_client)

    result = runner.invoke(openresty.app, ["config"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("GET", "/openresty/config", None, None, None),
    ]
    assert result.output == "worker_processes auto;\n"
