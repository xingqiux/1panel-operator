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


def test_device_help():
    from onepanel.cli.device import app

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    output = result.output.lower()
    assert "info" in output
    assert "timezone-options" in output
    assert "scan" in output


def test_root_help_includes_device_subcommand():
    from onepanel.cli import app as root_app

    result = runner.invoke(root_app, ["--help"])
    assert result.exit_code == 0
    assert "device" in result.output.lower()


def test_device_info_help():
    from onepanel.cli.device import app

    result = runner.invoke(app, ["info", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output


def test_device_timezone_options_help():
    from onepanel.cli.device import app

    result = runner.invoke(app, ["timezone-options", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output


def test_device_scan_help():
    from onepanel.cli.device import app

    result = runner.invoke(app, ["scan", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output


def test_device_info(monkeypatch):
    from onepanel.cli import device

    fake_client = _make_fake_client(
        {
            "data": {
                "dns": {"nameservers": ["1.1.1.1"]},
                "hosts": ["127.0.0.1 localhost"],
                "hostname": "node-1",
                "ntp": {"enabled": True},
                "user": "root",
                "timeZone": "America/Los_Angeles",
                "localTime": "2026-04-12T12:00:00-07:00",
                "swapMemoryTotal": 8589934592,
                "swapMemoryUsed": 1073741824,
                "swapMemoryAvailable": 7516192768,
                "swapDetails": {"type": "file"},
            }
        }
    )
    monkeypatch.setattr(device, "get_client", lambda ctx: fake_client)

    result = runner.invoke(device.app, ["info"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("POST", "/toolbox/device/base", {}, None, None),
    ]
    assert json.loads(result.output) == {
        "dns": {"nameservers": ["1.1.1.1"]},
        "hosts": ["127.0.0.1 localhost"],
        "hostname": "node-1",
        "localTime": "2026-04-12T12:00:00-07:00",
        "ntp": {"enabled": True},
        "swapMemoryTotal": 8589934592,
        "swapMemoryUsed": 1073741824,
        "timeZone": "America/Los_Angeles",
        "user": "root",
    }


def test_device_timezone_options(monkeypatch):
    from onepanel.cli import device

    fake_client = _make_fake_client(
        {
            "data": [
                {"label": "UTC", "value": "UTC"},
                {"label": "Los Angeles", "value": "America/Los_Angeles"},
            ]
        }
    )
    monkeypatch.setattr(device, "get_client", lambda ctx: fake_client)

    result = runner.invoke(device.app, ["timezone-options"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("GET", "/toolbox/device/zone/options", None, None, None),
    ]
    assert json.loads(result.output) == [
        {"label": "UTC", "value": "UTC"},
        {"label": "Los Angeles", "value": "America/Los_Angeles"},
    ]


def test_device_scan(monkeypatch):
    from onepanel.cli import device

    fake_client = _make_fake_client(
        {
            "data": {
                "status": "complete",
                "checked": 3,
                "issues": [],
            }
        }
    )
    monkeypatch.setattr(device, "get_client", lambda ctx: fake_client)

    result = runner.invoke(device.app, ["scan"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("POST", "/toolbox/scan", {}, None, None),
    ]
    assert json.loads(result.output) == {
        "checked": 3,
        "issues": [],
        "status": "complete",
    }
