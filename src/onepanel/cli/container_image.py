from __future__ import annotations

from typing import Any

import typer

from onepanel.cli import get_client, print_json

app = typer.Typer(help="Docker images and image repositories.")


def _image_summary(row: dict[str, Any]) -> dict[str, Any]:
    image_id = row.get("id")
    if image_id is None:
        image_id = row.get("ID") or row.get("imageID") or row.get("imageId")
    tags = row.get("tags")
    if tags is None:
        tags = row.get("repoTags") or row.get("RepoTags")
    size = row.get("size")
    if size is None:
        size = row.get("Size")
    created_at = row.get("createdAt")
    if created_at is None:
        created_at = row.get("created") or row.get("Created") or row.get("createTime")
    return {"id": image_id, "tags": tags, "size": size, "createdAt": created_at}


def _repo_summary(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": row.get("id"),
        "name": row.get("name"),
        "downloadUrl": row.get("downloadUrl"),
        "protocol": row.get("protocol"),
        "status": row.get("status"),
    }


@app.command("list")
def list_images(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
    page: int = typer.Option(1, help="Page number."),
    page_size: int = typer.Option(100, help="Items per page."),
) -> None:
    """Search images with pagination."""
    client = get_client(ctx)
    body: dict[str, Any] = {"page": page, "pageSize": page_size}
    response = client.request("POST", "/containers/image/search", body=body)
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return
    data = normalized.get("data", {})
    if not isinstance(data, dict):
        data = {}
    rows = data.get("items", [])
    if not isinstance(rows, list):
        rows = []
    items = [_image_summary(row) for row in rows if isinstance(row, dict)]
    print_json({"count": len(items), "total": data.get("total"), "items": items})


@app.command("all")
def list_all_images(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
) -> None:
    """List all images."""
    client = get_client(ctx)
    response = client.request("GET", "/containers/image/all")
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return
    data = normalized.get("data", [])
    if not isinstance(data, list) and not isinstance(data, dict):
        data = []
    print_json(data)


@app.command("repo-list")
def list_repos(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Print full API response."),
    page: int = typer.Option(1, help="Page number."),
    page_size: int = typer.Option(100, help="Items per page."),
) -> None:
    """Search image repositories with pagination."""
    client = get_client(ctx)
    body: dict[str, Any] = {"page": page, "pageSize": page_size}
    response = client.request("POST", "/containers/repo/search", body=body)
    normalized = client.normalize_response_payload(response)
    if raw:
        print_json(normalized)
        return
    data = normalized.get("data", {})
    if not isinstance(data, dict):
        data = {}
    rows = data.get("items", [])
    if not isinstance(rows, list):
        rows = []
    items = [_repo_summary(row) for row in rows if isinstance(row, dict)]
    print_json({"count": len(items), "total": data.get("total"), "items": items})
