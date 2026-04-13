from __future__ import annotations

from typing import Any

import typer

from onepanel.cli import get_client, print_json

app = typer.Typer(help="Website domain and Nginx config commands.")


def _domain_summary(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": row.get("id"),
        "domain": row.get("domain"),
        "port": row.get("port"),
        "ssl": row.get("ssl"),
    }


def _extract_rows(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return [row for row in data if isinstance(row, dict)]
    if isinstance(data, dict):
        rows = data.get("items")
        if isinstance(rows, list):
            return [row for row in rows if isinstance(row, dict)]
        rows = data.get("domains")
        if isinstance(rows, list):
            return [row for row in rows if isinstance(row, dict)]
    return []


@app.command("list")
def list_domains(
    ctx: typer.Context,
    website_id: int = typer.Argument(..., help="Website ID."),
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """List website domains for one website."""
    client = get_client(ctx)
    response = client.request("GET", f"/websites/domains/{website_id}")
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return

    rows = _extract_rows(normalized.get("data"))
    items = [_domain_summary(row) for row in rows]
    print_json({"count": len(items), "items": items})


@app.command("https")
def website_https(
    ctx: typer.Context,
    website_id: int = typer.Argument(..., help="Website ID."),
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Show HTTPS settings for one website."""
    client = get_client(ctx)
    response = client.request("GET", f"/websites/{website_id}/https")
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return

    data = normalized.get("data", {})
    if not isinstance(data, dict):
        data = {}
    print_json({
        "enable": data.get("enable"),
        "hsts": data.get("hsts"),
        "httpConfig": data.get("httpConfig"),
        "SSLProtocol": data.get("SSLProtocol"),
    })


@app.command("nginx-conf")
def nginx_conf(
    ctx: typer.Context,
    website_id: int = typer.Argument(..., help="Website ID."),
    config_type: str = typer.Argument(..., help="Config type."),
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Show an Nginx config section for one website."""
    client = get_client(ctx)
    response = client.request("GET", f"/websites/{website_id}/config/{config_type}")
    normalized = client.normalize_response_payload(response)
    print_json(normalized if raw else normalized.get("data"))
