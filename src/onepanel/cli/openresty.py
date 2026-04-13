from __future__ import annotations

from typing import Any

import typer

from onepanel.cli import get_client, print_json

app = typer.Typer(help="OpenResty status and config commands.")


def _status_data(normalized: dict[str, Any]) -> dict[str, Any]:
    data = normalized.get("data", {})
    if not isinstance(data, dict):
        data = {}
    return data


def _status_summary(data: dict[str, Any]) -> dict[str, Any]:
    return {
        "connections": data.get("connections"),
        "accepts": data.get("accepts"),
        "handled": data.get("handled"),
        "requests": data.get("requests"),
        "reading": data.get("reading"),
        "writing": data.get("writing"),
        "waiting": data.get("waiting"),
    }


@app.command("status")
def openresty_status(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Show OpenResty status."""
    client = get_client(ctx)
    response = client.request("GET", "/openresty")
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return

    data = _status_data(normalized)
    print_json(_status_summary(data))


@app.command("config")
def openresty_config(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Show OpenResty config."""
    client = get_client(ctx)
    response = client.request("GET", "/openresty/config")
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return

    data = normalized.get("data")
    if isinstance(data, str):
        typer.echo(data)
        return
    print_json(data)
