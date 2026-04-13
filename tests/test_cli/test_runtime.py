from __future__ import annotations

import json

from typer.testing import CliRunner

runner = CliRunner()


def _make_fake_client(normalized, response=None):
    class FakeClient:
        def __init__(self) -> None:
            self.requests: list[tuple[str, str, object, object, object]] = []

        def request(self, method, path, body=None, query=None, extra_headers=None):
            self.requests.append((method, path, body, query, extra_headers))
            if response is not None:
                return response
            return {"ok": True}

        def normalize_response_payload(self, response):
            return normalized

    return FakeClient()


def test_runtime_help():
    from onepanel.cli.runtime import app

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    output = result.output.lower()
    assert "list" in output
    assert "show" in output


def test_root_help_includes_runtime_subcommand():
    from onepanel.cli import app as root_app

    result = runner.invoke(root_app, ["--help"])
    assert result.exit_code == 0
    assert "runtime" in result.output.lower()


def test_runtime_list_help():
    from onepanel.cli.runtime import app

    result = runner.invoke(app, ["list", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output
    assert "--page" in result.output
    assert "--page-size" in result.output


def test_runtime_show_help():
    from onepanel.cli.runtime import app

    result = runner.invoke(app, ["show", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output


def test_runtime_list(monkeypatch):
    from onepanel.cli import runtime

    fake_client = _make_fake_client(
        {
            "data": {
                "total": 2,
                "items": [
                    {
                        "id": 1,
                        "name": "php-8.3",
                        "appDetailId": 101,
                        "type": "php",
                        "image": "php:8.3-fpm",
                        "status": "running",
                        "version": "8.3.10",
                        "createdAt": "2026-04-12T00:00:00Z",
                    },
                    {
                        "id": 2,
                        "name": "node-20",
                        "appDetailId": 102,
                        "type": "node",
                        "image": "node:20-alpine",
                        "status": "stopped",
                        "version": "20.18.0",
                        "createdAt": "2026-04-12T01:00:00Z",
                    },
                ],
            }
        }
    )
    monkeypatch.setattr(runtime, "get_client", lambda ctx: fake_client)

    result = runner.invoke(runtime.app, ["list", "--page", "3", "--page-size", "50"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("POST", "/runtimes/search", {"page": 3, "pageSize": 50}, None, None),
    ]
    assert json.loads(result.output) == {
        "count": 2,
        "total": 2,
        "items": [
            {
                "id": 1,
                "name": "php-8.3",
                "appDetailId": 101,
                "type": "php",
                "image": "php:8.3-fpm",
                "status": "running",
                "version": "8.3.10",
                "createdAt": "2026-04-12T00:00:00Z",
            },
            {
                "id": 2,
                "name": "node-20",
                "appDetailId": 102,
                "type": "node",
                "image": "node:20-alpine",
                "status": "stopped",
                "version": "20.18.0",
                "createdAt": "2026-04-12T01:00:00Z",
            },
        ],
    }


def test_runtime_show(monkeypatch):
    from onepanel.cli import runtime

    fake_client = _make_fake_client(
        {
            "data": {
                "id": 42,
                "name": "php-8.3",
                "type": "php",
                "image": "php:8.3-fpm",
                "status": "running",
                "version": "8.3.10",
                "phpConfig": {"memoryLimit": "256M"},
            }
        }
    )
    monkeypatch.setattr(runtime, "get_client", lambda ctx: fake_client)

    result = runner.invoke(runtime.app, ["show", "42"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("GET", "/runtimes/42", None, None, None),
    ]
    assert json.loads(result.output) == {
        "id": 42,
        "name": "php-8.3",
        "type": "php",
        "image": "php:8.3-fpm",
        "status": "running",
        "version": "8.3.10",
        "phpConfig": {"memoryLimit": "256M"},
    }
