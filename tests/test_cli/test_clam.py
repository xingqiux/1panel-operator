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


def test_clam_help():
    from onepanel.cli.clam import app

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    output = result.output.lower()
    assert "status" in output
    assert "list" in output
    assert "records" in output


def test_root_help_includes_clam_subcommand():
    from onepanel.cli import app as root_app

    result = runner.invoke(root_app, ["--help"])
    assert result.exit_code == 0
    assert "clam" in result.output.lower()


def test_clam_status_help():
    from onepanel.cli.clam import app

    result = runner.invoke(app, ["status", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output


def test_clam_list_help():
    from onepanel.cli.clam import app

    result = runner.invoke(app, ["list", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output
    assert "--page" in result.output
    assert "--page-size" in result.output


def test_clam_records_help():
    from onepanel.cli.clam import app

    result = runner.invoke(app, ["records", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output
    assert "--page" in result.output
    assert "--page-size" in result.output


def test_clam_status(monkeypatch):
    from onepanel.cli import clam

    fake_client = _make_fake_client(
        {
            "data": {
                "isExist": True,
                "isActive": False,
                "version": "1.4.2",
                "freshVersion": "1.4.3",
            }
        }
    )
    monkeypatch.setattr(clam, "get_client", lambda ctx: fake_client)

    result = runner.invoke(clam.app, ["status"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("GET", "/toolbox/clam/base", None, None, None),
    ]
    assert json.loads(result.output) == {
        "freshVersion": "1.4.3",
        "isActive": False,
        "isExist": True,
        "version": "1.4.2",
    }


def test_clam_list(monkeypatch):
    from onepanel.cli import clam

    fake_client = _make_fake_client(
        {
            "data": {
                "total": 2,
                "items": [
                    {
                        "id": 1,
                        "name": "web-root",
                        "path": "/var/www",
                        "infectedStrategy": "quarantine",
                        "status": "running",
                        "createdAt": "2026-04-12T00:00:00Z",
                    },
                    {
                        "id": 2,
                        "name": "uploads",
                        "path": "/srv/uploads",
                        "infectedStrategy": "delete",
                        "status": "stopped",
                        "createdAt": "2026-04-12T01:00:00Z",
                    },
                ],
            }
        }
    )
    monkeypatch.setattr(clam, "get_client", lambda ctx: fake_client)

    result = runner.invoke(clam.app, ["list", "--page", "2", "--page-size", "25"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("POST", "/toolbox/clam/search", {"page": 2, "pageSize": 25}, None, None),
    ]
    assert json.loads(result.output) == {
        "count": 2,
        "total": 2,
        "items": [
            {
                "id": 1,
                "name": "web-root",
                "path": "/var/www",
                "infectedStrategy": "quarantine",
                "status": "running",
                "createdAt": "2026-04-12T00:00:00Z",
            },
            {
                "id": 2,
                "name": "uploads",
                "path": "/srv/uploads",
                "infectedStrategy": "delete",
                "status": "stopped",
                "createdAt": "2026-04-12T01:00:00Z",
            },
        ],
    }


def test_clam_records(monkeypatch):
    from onepanel.cli import clam

    fake_client = _make_fake_client(
        {
            "data": {
                "total": 1,
                "items": [
                    {
                        "id": 11,
                        "name": "nightly-scan",
                        "clamID": 1,
                        "status": "success",
                        "startTime": "2026-04-12T02:00:00Z",
                        "endTime": "2026-04-12T02:05:00Z",
                    }
                ],
            }
        }
    )
    monkeypatch.setattr(clam, "get_client", lambda ctx: fake_client)

    result = runner.invoke(clam.app, ["records"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("POST", "/toolbox/clam/record/search", {"page": 1, "pageSize": 100}, None, None),
    ]
    assert json.loads(result.output) == {
        "count": 1,
        "total": 1,
        "items": [
            {
                "id": 11,
                "name": "nightly-scan",
                "clamID": 1,
                "status": "success",
                "startTime": "2026-04-12T02:00:00Z",
                "endTime": "2026-04-12T02:05:00Z",
            }
        ],
    }
