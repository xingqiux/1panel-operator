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


def test_system_help():
    from onepanel.cli.system import app

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    output = result.output.lower()
    assert "info" in output
    assert "interface" in output
    assert "basedir" in output
    assert "ssl-info" in output
    assert "snapshot-list" in output
    assert "group-list" in output


def test_root_help_includes_system_subcommand():
    from onepanel.cli import app as root_app

    result = runner.invoke(root_app, ["--help"])
    assert result.exit_code == 0
    assert "system" in result.output.lower()


def test_system_info_help():
    from onepanel.cli.system import app

    result = runner.invoke(app, ["info", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output


def test_system_interface_help():
    from onepanel.cli.system import app

    result = runner.invoke(app, ["interface", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output


def test_system_basedir_help():
    from onepanel.cli.system import app

    result = runner.invoke(app, ["basedir", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output


def test_system_ssl_info_help():
    from onepanel.cli.system import app

    result = runner.invoke(app, ["ssl-info", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output


def test_system_snapshot_list_help():
    from onepanel.cli.system import app

    result = runner.invoke(app, ["snapshot-list", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output
    assert "--page" in result.output
    assert "--page-size" in result.output


def test_system_group_list_help():
    from onepanel.cli.system import app

    result = runner.invoke(app, ["group-list", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output


def test_system_info(monkeypatch):
    from onepanel.cli import system

    fake_client = _make_fake_client(
        {
            "data": {
                "userName": "admin",
                "email": "admin@example.com",
                "systemIP": "10.0.0.5",
                "panelName": "1Panel",
                "theme": "light",
                "language": "en",
                "serverPort": "8080",
                "securityEntrance": "/secret",
                "expirationTime": "2026-04-12 00:00:00",
            }
        }
    )
    monkeypatch.setattr(system, "get_client", lambda ctx: fake_client)

    result = runner.invoke(system.app, ["info"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("POST", "/settings/search", {}, None, None),
    ]
    assert json.loads(result.output) == {
        "userName": "admin",
        "email": "admin@example.com",
        "systemIP": "10.0.0.5",
        "panelName": "1Panel",
        "theme": "light",
        "language": "en",
        "serverPort": "8080",
        "securityEntrance": "/secret",
        "expirationTime": "2026-04-12 00:00:00",
    }


def test_system_interface(monkeypatch):
    from onepanel.cli import system

    fake_client = _make_fake_client({"data": ["10.0.0.5", "192.168.1.10"]})
    monkeypatch.setattr(system, "get_client", lambda ctx: fake_client)

    result = runner.invoke(system.app, ["interface"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("GET", "/settings/interface", None, None, None),
    ]
    assert json.loads(result.output) == ["10.0.0.5", "192.168.1.10"]


def test_system_basedir(monkeypatch):
    from onepanel.cli import system

    fake_client = _make_fake_client({"data": "/opt/1panel"})
    monkeypatch.setattr(system, "get_client", lambda ctx: fake_client)

    result = runner.invoke(system.app, ["basedir"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("GET", "/settings/basedir", None, None, None),
    ]
    assert json.loads(result.output) == "/opt/1panel"


def test_system_ssl_info(monkeypatch):
    from onepanel.cli import system

    fake_client = _make_fake_client(
        {
            "data": {
                "domain": "example.com",
                "timeout": "2026-04-12T00:00:00Z",
                "rootPath": "/opt/1panel/1panel/secret/server.crt",
                "cert": "CERT",
                "key": "KEY",
                "sslID": 42,
            }
        }
    )
    monkeypatch.setattr(system, "get_client", lambda ctx: fake_client)

    result = runner.invoke(system.app, ["ssl-info"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("GET", "/settings/ssl/info", None, None, None),
    ]
    assert json.loads(result.output) == {
        "domain": "example.com",
        "timeout": "2026-04-12T00:00:00Z",
        "rootPath": "/opt/1panel/1panel/secret/server.crt",
        "cert": "CERT",
        "key": "KEY",
        "sslID": 42,
    }


def test_system_snapshot_list(monkeypatch):
    from onepanel.cli import system

    fake_client = _make_fake_client(
        {
            "data": {
                "total": 2,
                "items": [
                    {
                        "id": 101,
                        "name": "daily-db",
                        "description": "database backup",
                        "from": "system",
                        "status": "success",
                        "version": "1.0.0",
                        "createdAt": "2026-04-12T00:00:00Z",
                    },
                    {
                        "id": 102,
                        "name": "daily-files",
                        "description": "filesystem backup",
                        "from": "app",
                        "status": "failed",
                        "version": "1.0.1",
                        "createdAt": "2026-04-12T01:00:00Z",
                    },
                ],
            }
        }
    )
    monkeypatch.setattr(system, "get_client", lambda ctx: fake_client)

    result = runner.invoke(system.app, ["snapshot-list", "--page", "3", "--page-size", "50"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("POST", "/settings/snapshot/search", {"page": 3, "pageSize": 50}, None, None),
    ]
    assert json.loads(result.output) == {
        "count": 2,
        "total": 2,
        "items": [
            {
                "id": 101,
                "name": "daily-db",
                "description": "database backup",
                "from": "system",
                "status": "success",
                "version": "1.0.0",
                "createdAt": "2026-04-12T00:00:00Z",
            },
            {
                "id": 102,
                "name": "daily-files",
                "description": "filesystem backup",
                "from": "app",
                "status": "failed",
                "version": "1.0.1",
                "createdAt": "2026-04-12T01:00:00Z",
            },
        ],
    }


def test_system_group_list(monkeypatch):
    from onepanel.cli import system

    fake_client = _make_fake_client(
        {
            "data": [
                {"id": 1, "name": "host-a", "type": "host", "isDefault": True},
                {"id": 2, "name": "host-b", "type": "host", "isDefault": False},
            ]
        }
    )
    monkeypatch.setattr(system, "get_client", lambda ctx: fake_client)

    result = runner.invoke(system.app, ["group-list"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("POST", "/groups/search", {"type": "host"}, None, None),
    ]
    assert json.loads(result.output) == {
        "count": 2,
        "items": [
            {"id": 1, "name": "host-a", "type": "host"},
            {"id": 2, "name": "host-b", "type": "host"},
        ],
    }
