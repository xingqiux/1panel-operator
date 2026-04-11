from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import typer

from onepanel.cli import get_client, print_json
from onepanel.client import SAFE_METHODS
from onepanel.swagger import SwaggerParser

app = typer.Typer(help="Swagger discovery and raw API call tools.")
schema_app = typer.Typer(help="Inspect Swagger definitions.")
app.add_typer(schema_app, name="schema")


def _parse_key_values(items: list[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for item in items:
        if "=" not in item:
            raise typer.BadParameter(f"Expected KEY=VALUE format, got: {item}")
        key, value = item.split("=", 1)
        result[key] = value
    return result


def _load_body(body: str | None, body_file: str | None) -> Any | None:
    if body and body_file:
        raise typer.BadParameter("Use either --body or --body-file, not both.")
    if body:
        return json.loads(body)
    if body_file:
        return json.loads(Path(body_file).read_text(encoding="utf-8"))
    return None


def _get_parser(ctx: typer.Context) -> SwaggerParser:
    client = get_client(ctx)
    return SwaggerParser(client._swagger_cache)


@app.command("discover")
def discover(
    ctx: typer.Context,
    match: str = typer.Option(None, "--match", help="Filter by path, summary, or tag keyword."),
    tag: str = typer.Option(None, "--tag", help="Filter by Swagger tag."),
    limit: int = typer.Option(100, "--limit", help="Maximum number of endpoints to print."),
) -> None:
    """List operations from Swagger."""
    parser = _get_parser(ctx)
    operations = parser.list_operations(match=match, tag=tag)
    payload = [
        {
            "method": op.method,
            "path": op.path,
            "summary": op.summary,
            "tags": op.tags,
            "body_schema_ref": op.body_schema_ref,
            "path_params": op.path_params,
            "query_params": op.query_params,
            "response_schema_ref": op.response_schema_ref,
        }
        for op in operations[:limit]
    ]
    print_json(payload)


@schema_app.command("list")
def schema_list(
    ctx: typer.Context,
    match: str = typer.Option(None, "--match", help="Filter schema names by keyword."),
    limit: int = typer.Option(100, "--limit", help="Maximum number of schemas to print."),
) -> None:
    """List schema definition names."""
    parser = _get_parser(ctx)
    print_json(parser.list_schema_names(match=match)[:limit])


@schema_app.command("show")
def schema_show(
    ctx: typer.Context,
    name: str = typer.Argument(..., help="Definition name or #/definitions/ref."),
) -> None:
    """Print one schema definition."""
    parser = _get_parser(ctx)
    print_json(parser.get_schema(name))


@app.command("template")
def template(
    ctx: typer.Context,
    method: str = typer.Argument(..., help="HTTP method."),
    path: str = typer.Argument(..., help="Exact API path."),
) -> None:
    """Generate a request template from one Swagger operation."""
    parser = _get_parser(ctx)
    print_json(parser.build_operation_template(path, method))


@app.command("call")
def call(
    ctx: typer.Context,
    method: str = typer.Argument(..., help="HTTP method, e.g. GET or POST."),
    path: str = typer.Argument(..., help="API path like /websites/list or a full URL."),
    body: str = typer.Option(None, "--body", help="Inline JSON request body."),
    body_file: str = typer.Option(None, "--body-file", help="Path to a JSON file for the request body."),
    query: list[str] = typer.Option(None, "--query", help="Query string KEY=VALUE."),
    header: list[str] = typer.Option(None, "--header", help="Extra header KEY=VALUE."),
    confirm: bool = typer.Option(False, "--confirm", help="Allow write operations to execute."),
    assume_read: bool = typer.Option(
        False, "--assume-read",
        help="Allow non-GET requests that have been verified as read-only in Swagger.",
    ),
    data_only: bool = typer.Option(False, "--data-only", help="Print only the normalized data field."),
    raw_response: bool = typer.Option(False, "--raw-response", help="Print the unnormalized legacy response shape."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Print the planned request without executing it."),
) -> None:
    """Execute a raw API request."""
    client = get_client(ctx)
    http_method = method.upper()
    parsed_body = _load_body(body, body_file)
    parsed_query = _parse_key_values(query or [])
    parsed_headers = _parse_key_values(header or [])

    plan = client.plan(http_method, path, body=parsed_body, query=parsed_query)
    if assume_read:
        plan["write_operation"] = False

    if dry_run or (http_method not in SAFE_METHODS and not confirm and not assume_read):
        print_json(plan)
        raise typer.Exit(0 if dry_run else 2)

    response = client.request(
        http_method, path, body=parsed_body, query=parsed_query, extra_headers=parsed_headers,
    )

    if raw_response:
        print_json({
            "status_code": response["status_code"],
            "url": response["url"],
            "body": response["body"].get("json", response["body"].get("text")),
        })
        return

    normalized = client.normalize_response_payload(response)
    if data_only:
        print_json(normalized.get("data"))
        return
    print_json(normalized)
