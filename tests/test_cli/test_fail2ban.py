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


def test_fail2ban_help():
    from onepanel.cli.fail2ban import app

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    output = result.output.lower()
    assert "status" in output
    assert "conf" in output
    assert "list" in output


def test_root_help_includes_fail2ban_subcommand():
    from onepanel.cli import app as root_app

    result = runner.invoke(root_app, ["--help"])
    assert result.exit_code == 0
    assert "fail2ban" in result.output.lower()


def test_fail2ban_status_help():
    from onepanel.cli.fail2ban import app

    result = runner.invoke(app, ["status", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output


def test_fail2ban_conf_help():
    from onepanel.cli.fail2ban import app

    result = runner.invoke(app, ["conf", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output


def test_fail2ban_list_help():
    from onepanel.cli.fail2ban import app

    result = runner.invoke(app, ["list", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output
    assert "--status" in result.output
    assert "--page" in result.output
    assert "--page-size" in result.output


def test_fail2ban_status(monkeypatch):
    from onepanel.cli import fail2ban

    fake_client = _make_fake_client(
        {
            "data": {
                "isEnable": True,
                "isActive": True,
                "isExist": True,
                "version": "1.0.0",
                "maxRetry": 5,
                "banTime": 600,
                "findTime": 300,
            }
        }
    )
    monkeypatch.setattr(fail2ban, "get_client", lambda ctx: fake_client)

    result = runner.invoke(fail2ban.app, ["status"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("GET", "/toolbox/fail2ban/base", None, None, None),
    ]
    assert json.loads(result.output) == {
        "isEnable": True,
        "isActive": True,
        "isExist": True,
        "version": "1.0.0",
        "maxRetry": 5,
        "banTime": 600,
        "findTime": 300,
    }


def test_fail2ban_conf(monkeypatch):
    from onepanel.cli import fail2ban

    fake_client = _make_fake_client({"data": "DEFAULT-START\n[DEFAULT]\nbantime = 600"})
    monkeypatch.setattr(fail2ban, "get_client", lambda ctx: fake_client)

    result = runner.invoke(fail2ban.app, ["conf"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("GET", "/toolbox/fail2ban/load/conf", None, None, None),
    ]
    assert result.output == "DEFAULT-START\n[DEFAULT]\nbantime = 600\n"


def test_fail2ban_list(monkeypatch):
    from onepanel.cli import fail2ban

    fake_client = _make_fake_client(
        {
            "data": {
                "total": 1,
                "items": [
                    {
                        "id": 1,
                        "ip": "10.0.0.1",
                        "jail": "sshd",
                        "status": "banned",
                    }
                ],
            }
        }
    )
    monkeypatch.setattr(fail2ban, "get_client", lambda ctx: fake_client)

    result = runner.invoke(fail2ban.app, ["list", "--status", "banned", "--page", "2", "--page-size", "25"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        (
            "POST",
            "/toolbox/fail2ban/search",
            {"status": "banned", "page": 2, "pageSize": 25},
            None,
            None,
        ),
    ]
    assert json.loads(result.output) == {
        "total": 1,
        "items": [
            {
                "id": 1,
                "ip": "10.0.0.1",
                "jail": "sshd",
                "status": "banned",
            }
        ],
    }
