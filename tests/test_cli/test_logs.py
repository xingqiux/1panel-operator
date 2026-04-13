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


def test_logs_help():
    from onepanel.cli.logs import app

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    output = result.output.lower()
    assert "login" in output
    assert "operation" in output
    assert "system" in output
    assert "files" in output


def test_root_help_includes_logs_subcommand():
    from onepanel.cli import app as root_app

    result = runner.invoke(root_app, ["--help"])
    assert result.exit_code == 0
    assert "logs" in result.output.lower()


def test_logs_login_help():
    from onepanel.cli.logs import app

    result = runner.invoke(app, ["login", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output
    assert "--page" in result.output
    assert "--page-size" in result.output


def test_logs_operation_help():
    from onepanel.cli.logs import app

    result = runner.invoke(app, ["operation", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output
    assert "--page" in result.output
    assert "--page-size" in result.output


def test_logs_system_help():
    from onepanel.cli.logs import app

    result = runner.invoke(app, ["system", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output


def test_logs_files_help():
    from onepanel.cli.logs import app

    result = runner.invoke(app, ["files", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output


def test_logs_login(monkeypatch):
    from onepanel.cli import logs

    fake_client = _make_fake_client(
        {
            "data": {
                "total": 2,
                "items": [
                    {
                        "id": 1,
                        "ip": "10.0.0.1",
                        "address": "US",
                        "agent": "Chrome",
                        "status": "success",
                        "message": "ok",
                        "createdAt": "2026-04-12T00:00:00Z",
                    },
                    {
                        "id": 2,
                        "ip": "10.0.0.2",
                        "address": "CA",
                        "agent": "Firefox",
                        "status": "failed",
                        "message": "invalid password",
                        "createdAt": "2026-04-12T01:00:00Z",
                    },
                ],
            }
        }
    )
    monkeypatch.setattr(logs, "get_client", lambda ctx: fake_client)

    result = runner.invoke(logs.app, ["login", "--page", "2", "--page-size", "25"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("POST", "/logs/login", {"page": 2, "pageSize": 25}, None, None),
    ]
    assert json.loads(result.output) == {
        "count": 2,
        "total": 2,
        "items": [
            {
                "id": 1,
                "ip": "10.0.0.1",
                "address": "US",
                "agent": "Chrome",
                "status": "success",
                "message": "ok",
                "createdAt": "2026-04-12T00:00:00Z",
            },
            {
                "id": 2,
                "ip": "10.0.0.2",
                "address": "CA",
                "agent": "Firefox",
                "status": "failed",
                "message": "invalid password",
                "createdAt": "2026-04-12T01:00:00Z",
            },
        ],
    }


def test_logs_operation(monkeypatch):
    from onepanel.cli import logs

    fake_client = _make_fake_client(
        {
            "data": {
                "total": 1,
                "items": [
                    {
                        "id": 11,
                        "group": "system",
                        "source": "console",
                        "action": "restart",
                        "ip": "10.0.1.5",
                        "status": "success",
                        "message": "completed",
                        "createdAt": "2026-04-12T02:00:00Z",
                    }
                ],
            }
        }
    )
    monkeypatch.setattr(logs, "get_client", lambda ctx: fake_client)

    result = runner.invoke(logs.app, ["operation", "--page", "4", "--page-size", "10"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("POST", "/logs/operation", {"page": 4, "pageSize": 10}, None, None),
    ]
    assert json.loads(result.output) == {
        "count": 1,
        "total": 1,
        "items": [
            {
                "id": 11,
                "group": "system",
                "source": "console",
                "action": "restart",
                "ip": "10.0.1.5",
                "status": "success",
                "message": "completed",
                "createdAt": "2026-04-12T02:00:00Z",
            }
        ],
    }


def test_logs_system(monkeypatch):
    from onepanel.cli import logs

    fake_client = _make_fake_client({"data": "system line 1\nsystem line 2"})
    monkeypatch.setattr(logs, "get_client", lambda ctx: fake_client)

    result = runner.invoke(logs.app, ["system"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("POST", "/logs/system", {}, None, None),
    ]
    assert result.output == "system line 1\nsystem line 2\n"


def test_logs_files(monkeypatch):
    from onepanel.cli import logs

    fake_client = _make_fake_client({"data": ["messages.log", "messages.log.1"]})
    monkeypatch.setattr(logs, "get_client", lambda ctx: fake_client)

    result = runner.invoke(logs.app, ["files"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("GET", "/logs/system/files", None, None, None),
    ]
    assert json.loads(result.output) == ["messages.log", "messages.log.1"]
