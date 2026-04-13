from __future__ import annotations

from typing import Any

import typer

from onepanel.cli import get_client, print_json

app = typer.Typer(help="Device and system toolbox commands.")


def _device_data(normalized: dict[str, Any]) -> dict[str, Any]:
    data = normalized.get("data", {})
    if not isinstance(data, dict):
        data = {}
    return data


@app.command("info")
def device_info(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Show device base info."""
    client = get_client(ctx)
    response = client.request("POST", "/toolbox/device/base", body={})
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return

    data = _device_data(normalized)
    print_json({
        "dns": data.get("dns"),
        "hosts": data.get("hosts"),
        "hostname": data.get("hostname"),
        "ntp": data.get("ntp"),
        "user": data.get("user"),
        "timeZone": data.get("timeZone"),
        "localTime": data.get("localTime"),
        "swapMemoryTotal": data.get("swapMemoryTotal"),
        "swapMemoryUsed": data.get("swapMemoryUsed"),
    })


@app.command("timezone-options")
def timezone_options(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """List timezone options."""
    client = get_client(ctx)
    response = client.request("GET", "/toolbox/device/zone/options")
    normalized = client.normalize_response_payload(response)
    print_json(normalized if raw else normalized.get("data"))


@app.command("scan")
def scan_system(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Scan the system."""
    client = get_client(ctx)
    response = client.request("POST", "/toolbox/scan", body={})
    normalized = client.normalize_response_payload(response)
    print_json(normalized if raw else normalized.get("data"))
