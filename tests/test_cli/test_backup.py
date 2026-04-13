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


def test_backup_help():
    from onepanel.cli.backup import app

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    output = result.output.lower()
    assert "list" in output
    assert "records" in output


def test_root_help_includes_backup_subcommand():
    from onepanel.cli import app as root_app

    result = runner.invoke(root_app, ["--help"])
    assert result.exit_code == 0
    assert "backup" in result.output.lower()


def test_backup_list_help():
    from onepanel.cli.backup import app

    result = runner.invoke(app, ["list", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output


def test_backup_records_help():
    from onepanel.cli.backup import app

    result = runner.invoke(app, ["records", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output
    assert "--page" in result.output
    assert "--page-size" in result.output


def test_backup_list(monkeypatch):
    from onepanel.cli import backup

    fake_client = _make_fake_client(
        {
            "data": {
                "items": [
                    {
                        "id": 1,
                        "type": "s3",
                        "bucket": "daily-backups",
                        "varsJson": '{"region":"us-west-1"}',
                    },
                    {
                        "id": 2,
                        "type": "sftp",
                        "bucket": "remote-archive",
                        "varsJson": '{"host":"backup.example.com"}',
                    },
                ]
            }
        }
    )
    monkeypatch.setattr(backup, "get_client", lambda ctx: fake_client)

    result = runner.invoke(backup.app, ["list"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("GET", "/settings/backup/search", None, None, None),
    ]
    assert json.loads(result.output) == {
        "count": 2,
        "items": [
            {
                "id": 1,
                "type": "s3",
                "bucket": "daily-backups",
                "varsJson": '{"region":"us-west-1"}',
            },
            {
                "id": 2,
                "type": "sftp",
                "bucket": "remote-archive",
                "varsJson": '{"host":"backup.example.com"}',
            },
        ],
    }


def test_backup_records(monkeypatch):
    from onepanel.cli import backup

    fake_client = _make_fake_client(
        {
            "data": {
                "total": 2,
                "items": [
                    {
                        "id": 101,
                        "name": "daily-db",
                        "type": "database",
                        "source": "mysql",
                        "backupType": "full",
                        "fileName": "daily-db-2026-04-12.sql.gz",
                        "size": 1048576,
                        "createdAt": "2026-04-12T00:00:00Z",
                    },
                    {
                        "id": 102,
                        "name": "daily-files",
                        "type": "filesystem",
                        "source": "/var/www",
                        "backupType": "incremental",
                        "fileName": "daily-files-2026-04-12.tar.gz",
                        "size": 2097152,
                        "createdAt": "2026-04-12T01:00:00Z",
                    },
                ],
            }
        }
    )
    monkeypatch.setattr(backup, "get_client", lambda ctx: fake_client)

    result = runner.invoke(backup.app, ["records", "--page", "3", "--page-size", "50"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("POST", "/settings/backup/record/search", {"page": 3, "pageSize": 50}, None, None),
    ]
    assert json.loads(result.output) == {
        "count": 2,
        "total": 2,
        "items": [
            {
                "id": 101,
                "name": "daily-db",
                "type": "database",
                "source": "mysql",
                "backupType": "full",
                "fileName": "daily-db-2026-04-12.sql.gz",
                "size": 1048576,
                "createdAt": "2026-04-12T00:00:00Z",
            },
            {
                "id": 102,
                "name": "daily-files",
                "type": "filesystem",
                "source": "/var/www",
                "backupType": "incremental",
                "fileName": "daily-files-2026-04-12.tar.gz",
                "size": 2097152,
                "createdAt": "2026-04-12T01:00:00Z",
            },
        ],
    }
