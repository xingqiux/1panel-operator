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


def test_ftp_help():
    from onepanel.cli.ftp import app

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    output = result.output.lower()
    assert "status" in output
    assert "list" in output
    assert "logs" in output


def test_root_help_includes_ftp_subcommand():
    from onepanel.cli import app as root_app

    result = runner.invoke(root_app, ["--help"])
    assert result.exit_code == 0
    assert "ftp" in result.output.lower()


def test_ftp_status_help():
    from onepanel.cli.ftp import app

    result = runner.invoke(app, ["status", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output


def test_ftp_list_help():
    from onepanel.cli.ftp import app

    result = runner.invoke(app, ["list", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output
    assert "--page" in result.output
    assert "--page-size" in result.output


def test_ftp_logs_help():
    from onepanel.cli.ftp import app

    result = runner.invoke(app, ["logs", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output
    assert "--page" in result.output
    assert "--page-size" in result.output


def test_ftp_status(monkeypatch):
    from onepanel.cli import ftp

    fake_client = _make_fake_client({"data": {"isExist": True, "isActive": False}})
    monkeypatch.setattr(ftp, "get_client", lambda ctx: fake_client)

    result = runner.invoke(ftp.app, ["status"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("GET", "/toolbox/ftp/base", None, None, None),
    ]
    assert json.loads(result.output) == {
        "isExist": True,
        "isActive": False,
        "status": "inactive",
    }


def test_ftp_list(monkeypatch):
    from onepanel.cli import ftp

    fake_client = _make_fake_client(
        {
            "data": {
                "total": 2,
                "items": [
                    {
                        "id": 1,
                        "user": "ftp-web",
                        "path": "/srv/ftp/web",
                        "status": "enable",
                        "description": "website assets",
                        "createdAt": "2026-04-12T00:00:00Z",
                    },
                    {
                        "id": 2,
                        "user": "ftp-backup",
                        "path": "/srv/ftp/backup",
                        "status": "disable",
                        "description": "backup dropbox",
                        "createdAt": "2026-04-12T01:00:00Z",
                    },
                ],
            }
        }
    )
    monkeypatch.setattr(ftp, "get_client", lambda ctx: fake_client)

    result = runner.invoke(ftp.app, ["list", "--page", "3", "--page-size", "50"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("POST", "/toolbox/ftp/search", {"page": 3, "pageSize": 50}, None, None),
    ]
    assert json.loads(result.output) == {
        "count": 2,
        "total": 2,
        "items": [
            {
                "id": 1,
                "user": "ftp-web",
                "path": "/srv/ftp/web",
                "status": "enable",
                "description": "website assets",
                "createdAt": "2026-04-12T00:00:00Z",
            },
            {
                "id": 2,
                "user": "ftp-backup",
                "path": "/srv/ftp/backup",
                "status": "disable",
                "description": "backup dropbox",
                "createdAt": "2026-04-12T01:00:00Z",
            },
        ],
    }


def test_ftp_logs(monkeypatch):
    from onepanel.cli import ftp

    fake_client = _make_fake_client(
        {
            "data": {
                "total": 1,
                "items": [
                    {
                        "id": 11,
                        "ip": "10.0.0.20",
                        "user": "ftp-web",
                        "time": "2026-04-12T02:00:00Z",
                        "operation": "upload",
                        "status": "success",
                        "size": 4096,
                    }
                ],
            }
        }
    )
    monkeypatch.setattr(ftp, "get_client", lambda ctx: fake_client)

    result = runner.invoke(ftp.app, ["logs", "--page", "4", "--page-size", "25"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("POST", "/toolbox/ftp/log/search", {"page": 4, "pageSize": 25}, None, None),
    ]
    assert json.loads(result.output) == {
        "count": 1,
        "total": 1,
        "items": [
            {
                "id": 11,
                "ip": "10.0.0.20",
                "user": "ftp-web",
                "time": "2026-04-12T02:00:00Z",
                "operation": "upload",
                "status": "success",
                "size": 4096,
            }
        ],
    }
