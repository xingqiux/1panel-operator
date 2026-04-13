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


def test_file_mgr_help():
    from onepanel.cli.file_mgr import app

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    output = result.output.lower()
    assert "list" in output
    assert "tree" in output


def test_root_help_includes_file_subcommand():
    from onepanel.cli import app as root_app

    result = runner.invoke(root_app, ["--help"])
    assert result.exit_code == 0
    assert "file" in result.output.lower()


def test_file_mgr_list_help():
    from onepanel.cli.file_mgr import app

    result = runner.invoke(app, ["list", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output
    assert "--page" in result.output
    assert "--page-size" in result.output
    assert "path" in result.output.lower()


def test_file_mgr_tree_help():
    from onepanel.cli.file_mgr import app

    result = runner.invoke(app, ["tree", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output
    assert "path" in result.output.lower()


def test_file_mgr_list(monkeypatch):
    from onepanel.cli import file_mgr

    fake_client = _make_fake_client(
        {
            "data": {
                "items": [
                    {
                        "name": "app.log",
                        "isDir": False,
                        "size": 1024,
                        "mode": "644",
                        "user": "root",
                        "group": "root",
                        "modTime": "2026-04-12T00:00:00Z",
                    },
                    {
                        "name": "backups",
                        "isDir": True,
                        "size": 4096,
                        "mode": "755",
                        "user": "root",
                        "group": "root",
                        "modTime": "2026-04-12T01:00:00Z",
                    },
                ],
                "total": 2,
            }
        }
    )
    monkeypatch.setattr(file_mgr, "get_client", lambda ctx: fake_client)

    result = runner.invoke(file_mgr.app, ["list", "/var/log", "--page", "3", "--page-size", "50"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        (
            "POST",
            "/files/search",
            {"path": "/var/log", "expand": True, "page": 3, "pageSize": 50},
            None,
            None,
        ),
    ]
    assert json.loads(result.output) == {
        "path": "/var/log",
        "count": 2,
        "items": [
            {
                "name": "app.log",
                "isDir": False,
                "size": 1024,
                "mode": "644",
                "user": "root",
                "group": "root",
                "modTime": "2026-04-12T00:00:00Z",
            },
            {
                "name": "backups",
                "isDir": True,
                "size": 4096,
                "mode": "755",
                "user": "root",
                "group": "root",
                "modTime": "2026-04-12T01:00:00Z",
            },
        ],
    }


def test_file_mgr_tree(monkeypatch):
    from onepanel.cli import file_mgr

    fake_client = _make_fake_client(
        {
            "data": [
                {
                    "name": "var",
                    "path": "/var",
                    "isDir": True,
                    "children": [
                        {
                            "name": "log",
                            "path": "/var/log",
                            "isDir": True,
                            "children": [],
                        }
                    ],
                }
            ]
        }
    )
    monkeypatch.setattr(file_mgr, "get_client", lambda ctx: fake_client)

    result = runner.invoke(file_mgr.app, ["tree", "/var"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("POST", "/files/tree", {"path": "/var"}, None, None),
    ]
    assert json.loads(result.output) == [
        {
            "name": "var",
            "path": "/var",
            "isDir": True,
            "children": [
                {
                    "name": "log",
                    "path": "/var/log",
                    "isDir": True,
                    "children": [],
                }
            ],
        }
    ]
