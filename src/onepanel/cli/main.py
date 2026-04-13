from __future__ import annotations

import typer

from onepanel.cli import get_client, print_json
from onepanel.models import PanelAPIError

config_app = typer.Typer(help="Show resolved configuration.")


def ping(ctx: typer.Context) -> None:
    """Check connectivity using a safe API probe."""
    client = get_client(ctx)
    try:
        response = client.ping()
        print_json({
            "ok": True,
            "probe": "GET /websites/list",
            "status_code": response["status_code"],
            "url": response["url"],
        })
    except PanelAPIError as exc:
        output = {
            "ok": False,
            "error": str(exc),
            "status_code": exc.status_code,
        }
        if exc.api_message:
            output["api_message"] = exc.api_message
        if exc.hint:
            output["hint"] = exc.hint
        print_json(output)
        raise typer.Exit(1)


@config_app.command("show")
def config_show(
    ctx: typer.Context,
    reveal_key: bool = typer.Option(False, "--reveal-key", help="Print the full API key."),
) -> None:
    """Show the current configuration."""
    client = get_client(ctx)
    cfg = client.config
    print_json({
        "base_url": cfg.base_url,
        "api_key": cfg.api_key if reveal_key else cfg.masked_api_key,
        "timeout": cfg.timeout,
        "verify_tls": cfg.verify_tls,
        "swagger_cache_ttl_seconds": cfg.swagger_cache_ttl_seconds,
    })


@config_app.command("cache")
def config_cache(ctx: typer.Context) -> None:
    """Show Swagger cache status."""
    client = get_client(ctx)
    print_json(client.cache_info())
