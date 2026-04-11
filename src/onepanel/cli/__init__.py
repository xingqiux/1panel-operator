from __future__ import annotations

import json

import typer

from onepanel.client import PanelClient
from onepanel.config import PanelConfig, PanelConfigError
from onepanel.log import setup_logging

app = typer.Typer(name="1panel", help="Operate a 1Panel instance through its API.")


@app.callback()
def main_callback(
    ctx: typer.Context,
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output."),
    debug: bool = typer.Option(False, "--debug", help="Enable debug output."),
) -> None:
    setup_logging(verbose=verbose, debug=debug)
    try:
        config = PanelConfig()
        ctx.ensure_object(dict)
        ctx.obj = {"client": PanelClient(config)}
    except PanelConfigError as e:
        typer.echo(f"Configuration error: {e}", err=True)
        raise typer.Exit(1)


def get_client(ctx: typer.Context) -> PanelClient:
    return ctx.obj["client"]


def print_json(value) -> None:
    typer.echo(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))


from onepanel.cli.main import config_app, ping  # noqa: E402
from onepanel.cli import api, application, website  # noqa: E402
from onepanel.cli import container, dashboard, firewall, host  # noqa: E402

app.command("ping")(ping)
app.add_typer(config_app, name="config")
app.add_typer(website.app, name="website")
app.add_typer(application.app, name="app")
app.add_typer(container.app, name="container")
app.add_typer(dashboard.app, name="dashboard")
app.add_typer(host.app, name="host")
app.add_typer(firewall.app, name="firewall")
app.add_typer(api.app, name="api")
