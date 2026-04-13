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


def test_cronjob_help():
    from onepanel.cli.cronjob import app

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    output = result.output.lower()
    assert "list" in output
    assert "show" in output


def test_root_help_includes_cronjob_subcommand():
    from onepanel.cli import app as root_app

    result = runner.invoke(root_app, ["--help"])
    assert result.exit_code == 0
    assert "cronjob" in result.output.lower()


def test_cronjob_list_help():
    from onepanel.cli.cronjob import app

    result = runner.invoke(app, ["list", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output
    assert "--page" in result.output
    assert "--page-size" in result.output


def test_cronjob_show_help():
    from onepanel.cli.cronjob import app

    result = runner.invoke(app, ["show", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output


def test_cronjob_list(monkeypatch):
    from onepanel.cli import cronjob

    fake_client = _make_fake_client(
        {
            "data": {
                "total": 2,
                "items": [
                    {
                        "id": 1,
                        "name": "daily-backup",
                        "type": "backup",
                        "specType": "day",
                        "spec": "0 1 * * *",
                        "status": "enabled",
                        "lastRecordTime": "2026-04-12T00:00:00Z",
                        "createdAt": "2026-04-10T00:00:00Z",
                    },
                    {
                        "id": 2,
                        "name": "weekly-cleanup",
                        "type": "clean",
                        "specType": "week",
                        "spec": "0 3 * * 0",
                        "status": "disabled",
                        "lastRecordTime": "2026-04-11T03:00:00Z",
                        "createdAt": "2026-04-09T00:00:00Z",
                    },
                ],
            }
        }
    )
    monkeypatch.setattr(cronjob, "get_client", lambda ctx: fake_client)

    result = runner.invoke(cronjob.app, ["list", "--page", "4", "--page-size", "25"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("POST", "/cronjobs/search", {"page": 4, "pageSize": 25}, None, None),
    ]
    assert json.loads(result.output) == {
        "count": 2,
        "total": 2,
        "items": [
            {
                "id": 1,
                "name": "daily-backup",
                "type": "backup",
                "specType": "day",
                "spec": "0 1 * * *",
                "status": "enabled",
                "lastRecordTime": "2026-04-12T00:00:00Z",
                "createdAt": "2026-04-10T00:00:00Z",
            },
            {
                "id": 2,
                "name": "weekly-cleanup",
                "type": "clean",
                "specType": "week",
                "spec": "0 3 * * 0",
                "status": "disabled",
                "lastRecordTime": "2026-04-11T03:00:00Z",
                "createdAt": "2026-04-09T00:00:00Z",
            },
        ],
    }


def test_cronjob_show(monkeypatch):
    from onepanel.cli import cronjob

    fake_client = _make_fake_client(
        {
            "data": {
                "id": 42,
                "name": "daily-backup",
                "type": "backup",
                "specType": "day",
                "spec": "0 1 * * *",
                "status": "enabled",
                "lastRecordTime": "2026-04-12T00:00:00Z",
                "createdAt": "2026-04-10T00:00:00Z",
                "retention": 7,
                "labels": ["prod", "backup"],
            }
        }
    )
    monkeypatch.setattr(cronjob, "get_client", lambda ctx: fake_client)

    result = runner.invoke(cronjob.app, ["show", "42"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("GET", "/cronjobs/42", None, None, None),
    ]
    assert json.loads(result.output) == {
        "id": 42,
        "name": "daily-backup",
        "type": "backup",
        "specType": "day",
        "spec": "0 1 * * *",
        "status": "enabled",
        "lastRecordTime": "2026-04-12T00:00:00Z",
        "createdAt": "2026-04-10T00:00:00Z",
        "retention": 7,
        "labels": ["prod", "backup"],
    }
