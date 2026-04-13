from __future__ import annotations

from typing import Any

import typer

from onepanel.cli import get_client, print_json

app = typer.Typer(help="Fail2ban management commands.")


def _fail2ban_data(normalized: dict[str, Any]) -> dict[str, Any]:
    data = normalized.get("data", {})
    if not isinstance(data, dict):
        data = {}
    return data


@app.command("status")
def fail2ban_status(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Show Fail2ban status."""
    client = get_client(ctx)
    response = client.request("GET", "/toolbox/fail2ban/base")
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return

    data = _fail2ban_data(normalized)
    print_json({
        "isEnable": data.get("isEnable"),
        "isActive": data.get("isActive"),
        "isExist": data.get("isExist"),
        "version": data.get("version"),
        "maxRetry": data.get("maxRetry"),
        "banTime": data.get("banTime"),
        "findTime": data.get("findTime"),
    })


@app.command("conf")
def fail2ban_conf(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Show Fail2ban configuration."""
    client = get_client(ctx)
    response = client.request("GET", "/toolbox/fail2ban/load/conf")
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return

    data = normalized.get("data")
    if isinstance(data, str):
        typer.echo(data)
        return
    print_json(data)


@app.command("list")
def fail2ban_list(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
    status: str = typer.Option("banned", "--status", help="Filter: banned or ignore."),
    page: int = typer.Option(1, "--page", help="Page number."),
    page_size: int = typer.Option(100, "--page-size", help="Items per page."),
) -> None:
    """List Fail2ban banned or ignored IPs."""
    client = get_client(ctx)
    body: dict[str, Any] = {"status": status, "page": page, "pageSize": page_size}
    response = client.request("POST", "/toolbox/fail2ban/search", body=body)
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return
    print_json(normalized.get("data"))
