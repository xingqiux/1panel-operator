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


def test_ssh_help():
    from onepanel.cli.ssh import app

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    output = result.output.lower()
    assert "status" in output
    assert "conf" in output
    assert "logs" in output


def test_ssh_status_help():
    from onepanel.cli.ssh import app

    result = runner.invoke(app, ["status", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output


def test_ssh_conf_help():
    from onepanel.cli.ssh import app

    result = runner.invoke(app, ["conf", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output


def test_ssh_logs_help():
    from onepanel.cli.ssh import app

    result = runner.invoke(app, ["logs", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output
    assert "--status" in result.output
    assert "--page" in result.output
    assert "--page-size" in result.output


def test_root_help_includes_ssh_subcommand():
    from onepanel.cli import app as root_app

    result = runner.invoke(root_app, ["--help"])
    assert result.exit_code == 0
    assert "ssh" in result.output.lower()


def test_ssh_status(monkeypatch):
    from onepanel.cli import ssh

    fake_client = _make_fake_client(
        {
            "data": {
                "status": "enabled",
                "port": 22,
                "listenAddress": "0.0.0.0",
                "passwordAuthentication": "yes",
                "pubkeyAuthentication": "yes",
                "permitRootLogin": "no",
                "useDNS": "no",
            }
        }
    )
    monkeypatch.setattr(ssh, "get_client", lambda ctx: fake_client)

    result = runner.invoke(ssh.app, ["status"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("POST", "/hosts/ssh/search", {}, None, None),
    ]
    assert json.loads(result.output) == {
        "status": "enabled",
        "port": 22,
        "listenAddress": "0.0.0.0",
        "passwordAuthentication": "yes",
        "pubkeyAuthentication": "yes",
        "permitRootLogin": "no",
        "useDNS": "no",
    }


def test_ssh_conf(monkeypatch):
    from onepanel.cli import ssh

    fake_client = _make_fake_client({"data": "Port 22\nPermitRootLogin yes"})
    monkeypatch.setattr(ssh, "get_client", lambda ctx: fake_client)

    result = runner.invoke(ssh.app, ["conf"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("GET", "/hosts/ssh/conf", None, None, None),
    ]
    assert result.output == "Port 22\nPermitRootLogin yes\n"


def test_ssh_logs(monkeypatch):
    from onepanel.cli import ssh

    fake_client = _make_fake_client(
        {
            "data": {
                "successfulCount": 9,
                "failedCount": 1,
                "logs": [
                    {"id": 1, "status": "Success", "addr": "10.0.0.1"},
                    {"id": 2, "status": "Failed", "addr": "10.0.0.2"},
                ],
            }
        }
    )
    monkeypatch.setattr(ssh, "get_client", lambda ctx: fake_client)

    result = runner.invoke(ssh.app, ["logs", "--status", "Success", "--page", "2", "--page-size", "25"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("POST", "/hosts/ssh/log", {"Status": "Success", "page": 2, "pageSize": 25}, None, None),
    ]
    assert json.loads(result.output) == {
        "successfulCount": 9,
        "failedCount": 1,
        "logs": [
            {"id": 1, "status": "Success", "addr": "10.0.0.1"},
            {"id": 2, "status": "Failed", "addr": "10.0.0.2"},
        ],
    }
