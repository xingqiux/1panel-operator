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


def test_database_help():
    from onepanel.cli.database import app

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    output = result.output.lower()
    assert "list" in output
    assert "show" in output
    assert "mysql-list" in output
    assert "mysql-status" in output
    assert "pg-list" in output
    assert "redis-status" in output
    assert "redis-conf" in output
    assert "redis-commands" in output


def test_root_help_includes_database_subcommand():
    from onepanel.cli import app as root_app

    result = runner.invoke(root_app, ["--help"])
    assert result.exit_code == 0
    assert "database" in result.output.lower()


def test_database_list(monkeypatch):
    from onepanel.cli import database

    fake_client = _make_fake_client(
        {
            "data": {
                "total": 2,
                "items": [
                    {
                        "id": 1,
                        "name": "main",
                        "type": "mysql",
                        "version": "8.0",
                        "from": "system",
                        "address": "127.0.0.1",
                        "port": 3306,
                        "status": "running",
                        "createdAt": "2026-04-12T00:00:00Z",
                    },
                    {
                        "id": 2,
                        "name": "cache",
                        "type": "redis",
                        "version": "7",
                        "from": "app",
                        "address": "127.0.0.1",
                        "port": 6379,
                        "status": "stopped",
                        "createdAt": "2026-04-12T00:00:01Z",
                    },
                ],
            }
        }
    )
    monkeypatch.setattr(database, "get_client", lambda ctx: fake_client)

    result = runner.invoke(database.app, ["list", "--page", "2", "--page-size", "25"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("POST", "/databases/db/search", {"page": 2, "pageSize": 25}, None, None),
    ]
    assert json.loads(result.output) == {
        "count": 2,
        "total": 2,
        "items": [
            {
                "id": 1,
                "name": "main",
                "type": "mysql",
                "version": "8.0",
                "from": "system",
                "address": "127.0.0.1",
                "port": 3306,
                "status": "running",
                "createdAt": "2026-04-12T00:00:00Z",
            },
            {
                "id": 2,
                "name": "cache",
                "type": "redis",
                "version": "7",
                "from": "app",
                "address": "127.0.0.1",
                "port": 6379,
                "status": "stopped",
                "createdAt": "2026-04-12T00:00:01Z",
            },
        ],
    }


def test_database_show(monkeypatch):
    from onepanel.cli import database

    fake_client = _make_fake_client(
        {
            "data": {
                "id": 10,
                "name": "main",
                "type": "mysql",
                "version": "8.0",
                "from": "system",
                "address": "127.0.0.1",
                "port": 3306,
                "status": "running",
                "createdAt": "2026-04-12T00:00:00Z",
            }
        }
    )
    monkeypatch.setattr(database, "get_client", lambda ctx: fake_client)

    result = runner.invoke(database.app, ["show", "main"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("GET", "/databases/db/main", None, None, None),
    ]
    assert json.loads(result.output) == {
        "id": 10,
        "name": "main",
        "type": "mysql",
        "version": "8.0",
        "from": "system",
        "address": "127.0.0.1",
        "port": 3306,
        "status": "running",
        "createdAt": "2026-04-12T00:00:00Z",
    }


def test_database_mysql_list(monkeypatch):
    from onepanel.cli import database

    fake_client = _make_fake_client(
        {
            "data": {
                "total": 1,
                "items": [
                    {
                        "id": 3,
                        "name": "app",
                        "mysqlName": "app_db",
                        "format": "utf8mb4",
                        "username": "appuser",
                        "permission": "read-write",
                        "description": "application database",
                        "createdAt": "2026-04-12T00:00:02Z",
                    }
                ],
            }
        }
    )
    monkeypatch.setattr(database, "get_client", lambda ctx: fake_client)

    result = runner.invoke(database.app, ["mysql-list", "--page", "3", "--page-size", "50"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("POST", "/databases/search", {"page": 3, "pageSize": 50}, None, None),
    ]
    assert json.loads(result.output) == {
        "count": 1,
        "total": 1,
        "items": [
            {
                "id": 3,
                "name": "app",
                "mysqlName": "app_db",
                "format": "utf8mb4",
                "username": "appuser",
                "permission": "read-write",
                "description": "application database",
                "createdAt": "2026-04-12T00:00:02Z",
            }
        ],
    }


def test_database_mysql_status(monkeypatch):
    from onepanel.cli import database

    fake_client = _make_fake_client(
        {
            "data": {
                "status": "running",
                "version": "8.0",
                "containerName": "mysql-main",
            }
        }
    )
    monkeypatch.setattr(database, "get_client", lambda ctx: fake_client)

    result = runner.invoke(database.app, ["mysql-status", "main"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("POST", "/databases/status", {"name": "main", "type": "mysql"}, None, None),
    ]
    assert json.loads(result.output) == {
        "status": "running",
        "version": "8.0",
        "containerName": "mysql-main",
    }


def test_database_pg_list(monkeypatch):
    from onepanel.cli import database

    fake_client = _make_fake_client(
        {
            "data": {
                "total": 1,
                "items": [
                    {
                        "id": 4,
                        "name": "analytics",
                        "pgName": "analytics_db",
                        "format": "UTF8",
                        "username": "pguser",
                        "description": "reporting database",
                        "createdAt": "2026-04-12T00:00:03Z",
                    }
                ],
            }
        }
    )
    monkeypatch.setattr(database, "get_client", lambda ctx: fake_client)

    result = runner.invoke(database.app, ["pg-list"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("POST", "/databases/pg/search", {"page": 1, "pageSize": 100}, None, None),
    ]
    assert json.loads(result.output) == {
        "count": 1,
        "total": 1,
        "items": [
            {
                "id": 4,
                "name": "analytics",
                "pgName": "analytics_db",
                "format": "UTF8",
                "username": "pguser",
                "description": "reporting database",
                "createdAt": "2026-04-12T00:00:03Z",
            }
        ],
    }


def test_database_redis_status(monkeypatch):
    from onepanel.cli import database

    fake_client = _make_fake_client(
        {
            "data": {
                "status": "running",
                "port": 6379,
                "version": "7.2",
            }
        }
    )
    monkeypatch.setattr(database, "get_client", lambda ctx: fake_client)

    result = runner.invoke(database.app, ["redis-status", "cache"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("POST", "/databases/redis/status", {"name": "cache"}, None, None),
    ]
    assert json.loads(result.output) == {
        "status": "running",
        "port": 6379,
        "version": "7.2",
    }


def test_database_redis_conf(monkeypatch):
    from onepanel.cli import database

    fake_client = _make_fake_client(
        {
            "data": "bind 0.0.0.0\nport 6379\n",
        }
    )
    monkeypatch.setattr(database, "get_client", lambda ctx: fake_client)

    result = runner.invoke(database.app, ["redis-conf", "cache"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("POST", "/databases/redis/conf", {"name": "cache"}, None, None),
    ]
    assert json.loads(result.output) == "bind 0.0.0.0\nport 6379\n"


def test_database_redis_commands(monkeypatch):
    from onepanel.cli import database

    fake_client = _make_fake_client(
        {
            "data": [
                {"id": 1, "name": "set", "command": "SET key value"},
                {"id": 2, "name": "get", "command": "GET key"},
            ]
        }
    )
    monkeypatch.setattr(database, "get_client", lambda ctx: fake_client)

    result = runner.invoke(database.app, ["redis-commands"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("GET", "/hosts/command/redis", None, None, None),
    ]
    assert json.loads(result.output) == {
        "count": 2,
        "items": [
            {"id": 1, "name": "set", "command": "SET key value"},
            {"id": 2, "name": "get", "command": "GET key"},
        ],
    }
