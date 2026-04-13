from __future__ import annotations

from typing import Any

import typer

from onepanel.cli import get_client, print_json

app = typer.Typer(help="SSH management commands.")


def _ssh_data(normalized: dict[str, Any]) -> dict[str, Any]:
    data = normalized.get("data", {})
    if not isinstance(data, dict):
        data = {}
    return data


@app.command("status")
def ssh_status(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Show SSH status."""
    client = get_client(ctx)
    response = client.request("POST", "/hosts/ssh/search", body={})
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return

    data = _ssh_data(normalized)
    print_json({
        "status": data.get("status"),
        "port": data.get("port"),
        "listenAddress": data.get("listenAddress"),
        "passwordAuthentication": data.get("passwordAuthentication"),
        "pubkeyAuthentication": data.get("pubkeyAuthentication"),
        "permitRootLogin": data.get("permitRootLogin"),
        "useDNS": data.get("useDNS"),
    })


@app.command("conf")
def ssh_conf(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Show raw SSH config text."""
    client = get_client(ctx)
    response = client.request("GET", "/hosts/ssh/conf")
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return

    data = normalized.get("data")
    if isinstance(data, str):
        typer.echo(data)
        return
    print_json(data)


@app.command("logs")
def ssh_logs(
    ctx: typer.Context,
    status: str = typer.Option("All", "--status", help="Filter: All, Success, Failed."),
    page: int = typer.Option(1, "--page", help="Page number."),
    page_size: int = typer.Option(100, "--page-size", help="Items per page."),
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Search SSH login logs."""
    client = get_client(ctx)
    body: dict[str, Any] = {"Status": status, "page": page, "pageSize": page_size}
    response = client.request("POST", "/hosts/ssh/log", body=body)
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return

    data = _ssh_data(normalized)
    print_json({
        "successfulCount": data.get("successfulCount"),
        "failedCount": data.get("failedCount"),
        "logs": data.get("logs", []),
    })
