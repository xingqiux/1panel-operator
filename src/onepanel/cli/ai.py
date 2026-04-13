from __future__ import annotations

from typing import Any

import typer

from onepanel.cli import get_client, print_json

app = typer.Typer(help="AI GPU and Ollama model commands.")

_MODEL_FIELDS = ("id", "name", "size", "status", "createdAt")


def _normalized_response(client: Any, response: Any) -> Any:
    if not isinstance(response, dict):
        return response
    return client.normalize_response_payload(response)


def _summary(row: dict[str, Any], fields: tuple[str, ...]) -> dict[str, Any]:
    return {field: row.get(field) for field in fields if field in row}


def _extract_rows(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return [row for row in data if isinstance(row, dict)]
    if isinstance(data, dict):
        for key in ("items", "list", "models"):
            rows = data.get(key)
            if isinstance(rows, list):
                return [row for row in rows if isinstance(row, dict)]
    return []


@app.command("gpu")
def gpu_cmd(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """Show GPU and XPU status."""
    client = get_client(ctx)
    response = client.request("GET", "/ai/gpu")
    normalized = _normalized_response(client, response)
    if raw or not isinstance(normalized, dict):
        print_json(normalized)
        return

    data = normalized.get("data", {})
    if not isinstance(data, dict) and not isinstance(data, list):
        data = {}
    print_json(data)


@app.command("models")
def models_cmd(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """List Ollama models."""
    client = get_client(ctx)
    response = client.request("GET", "/ai/ollama/models")
    normalized = _normalized_response(client, response)
    if raw or not isinstance(normalized, dict):
        print_json(normalized)
        return

    data = normalized.get("data", {})
    rows = _extract_rows(data)
    items = [_summary(row, _MODEL_FIELDS) for row in rows]
    payload: dict[str, Any] = {"count": len(items), "items": items}
    if isinstance(data, dict) and "total" in data:
        payload["total"] = data.get("total")
    print_json(payload)
