from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from panel_client import PanelClient
from panel_config import load_config


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "references" / "generated"


def fetch_spec() -> tuple[Dict[str, Any], str]:
    client = PanelClient(load_config())
    spec = client.swagger_spec()
    resolved_url = client.swagger_url()
    public_url = resolved_url.replace(client.config.base_url, "<configured-base-url>")
    return spec, public_url


def slugify(text: str) -> str:
    value = text.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "untagged"


def extract_operations(spec: Dict[str, Any]) -> List[Dict[str, Any]]:
    operations: List[Dict[str, Any]] = []
    for path, methods in spec.get("paths", {}).items():
        for method, op in methods.items():
            body_schema_ref = None
            path_params: List[str] = []
            query_params: List[str] = []
            for param in op.get("parameters", []):
                if param.get("in") == "body":
                    body_schema_ref = param.get("schema", {}).get("$ref")
                elif param.get("in") == "path":
                    path_params.append(param.get("name", ""))
                elif param.get("in") == "query":
                    query_params.append(param.get("name", ""))

            response_schema_ref = None
            for _, response in op.get("responses", {}).items():
                schema = response.get("schema", {})
                if "$ref" in schema:
                    response_schema_ref = schema["$ref"]
                    break
                items = schema.get("items", {})
                if "$ref" in items:
                    response_schema_ref = items["$ref"]
                    break

            operations.append(
                {
                    "method": method.upper(),
                    "path": path,
                    "summary": op.get("summary", ""),
                    "tags": op.get("tags", ["(untagged)"]),
                    "body_schema_ref": body_schema_ref,
                    "path_params": path_params,
                    "query_params": query_params,
                    "response_schema_ref": response_schema_ref,
                }
            )

    operations.sort(key=lambda item: (item["tags"][0], item["path"], item["method"]))
    return operations


def build_tag_index(operations: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    grouped: Dict[str, List[Dict[str, Any]]] = {}
    for op in operations:
        for tag in op["tags"] or ["(untagged)"]:
            grouped.setdefault(tag, []).append(op)
    return dict(sorted(grouped.items(), key=lambda item: (-len(item[1]), item[0].lower())))


def build_path_index(operations: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    grouped: Dict[str, List[Dict[str, Any]]] = {}
    for op in operations:
        grouped.setdefault(op["path"], []).append(op)
    return dict(sorted(grouped.items(), key=lambda item: item[0]))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_markdown(tag_index: Dict[str, List[Dict[str, Any]]], definitions: Dict[str, Any]) -> None:
    lines = [
        "# 1Panel Swagger Catalog",
        "",
        f"- 标签数：`{len(tag_index)}`",
        f"- 接口数：`{sum(len(items) for items in tag_index.values())}`",
        f"- Schema 数：`{len(definitions)}`",
        "",
        "## Tags",
        "",
    ]
    for tag, items in tag_index.items():
        slug = slugify(tag)
        lines.append(f"- [{tag}](tags/{slug}.md)：`{len(items)}`")

    lines.append("")
    (OUT_DIR / "catalog.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    tags_dir = OUT_DIR / "tags"
    tags_dir.mkdir(parents=True, exist_ok=True)
    for tag, items in tag_index.items():
        slug = slugify(tag)
        tag_lines = [f"# {tag}", "", f"- 接口数：`{len(items)}`", "", "| Method | Path | Summary | Body Schema | Response Schema |", "| --- | --- | --- | --- | --- |"]
        for op in items:
            tag_lines.append(
                f"| `{op['method']}` | `{op['path']}` | {op['summary'] or '-'} | `{op['body_schema_ref'] or '-'}` | `{op['response_schema_ref'] or '-'}` |"
            )
        (tags_dir / f"{slug}.md").write_text("\n".join(tag_lines) + "\n", encoding="utf-8")


def write_verbose_index(spec: Dict[str, Any], tag_index: Dict[str, List[Dict[str, Any]]], metadata: Dict[str, Any]) -> None:
    lines = [
        "# 1Panel Swagger API Index",
        "",
        f"Generated from `{metadata['source_url']}` on {metadata['generated_at']}",
        "",
    ]

    for tag, items in tag_index.items():
        lines.append(f"## Tag: {tag}")
        lines.append("")
        for op in items:
            body_value = op["body_schema_ref"] or "None"
            response_value = op["response_schema_ref"] or "None"
            path_params = ", ".join(op["path_params"]) if op["path_params"] else "None"
            query_params = ", ".join(op["query_params"]) if op["query_params"] else "None"
            lines.append(f"- **`{op['method']}` {op['path']}** — {op['summary'] or '-'}")
            lines.append(f"  - Tags: {', '.join(op['tags']) if op['tags'] else 'None'}")
            lines.append(f"  - Body schemas: `{body_value}`")
            lines.append(f"  - Responses: `200` → `{response_value}`")
            lines.append(f"  - Path params: {path_params}")
            lines.append(f"  - Query params: {query_params}")
        lines.append("")

    (OUT_DIR / "swagger-index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    spec, public_source_url = fetch_spec()
    operations = extract_operations(spec)
    tag_index = build_tag_index(operations)
    path_index = build_path_index(operations)
    generated_at = datetime.now(timezone.utc).isoformat()

    summary = {
        "swagger": spec.get("swagger"),
        "basePath": spec.get("basePath"),
        "path_count": len(spec.get("paths", {})),
        "operation_count": len(operations),
        "definition_count": len(spec.get("definitions", {})),
        "tags": [{"tag": tag, "count": len(items), "slug": slugify(tag)} for tag, items in tag_index.items()],
    }
    metadata = {
        "source_url": public_source_url,
        "openapi": spec.get("swagger"),
        "generated_at": generated_at,
        "operation_count": len(operations),
    }
    swagger_by_tag = {
        "metadata": metadata,
        "tags": tag_index,
    }
    swagger_by_path = {
        "metadata": metadata,
        "paths": path_index,
    }

    write_json(OUT_DIR / "summary.json", summary)
    write_json(OUT_DIR / "operations.json", operations)
    write_json(OUT_DIR / "definitions.json", sorted(spec.get("definitions", {}).keys()))
    write_json(OUT_DIR / "swagger-by-tag.json", swagger_by_tag)
    write_json(OUT_DIR / "swagger-by-path.json", swagger_by_path)
    write_markdown(tag_index, spec.get("definitions", {}))
    write_verbose_index(spec, tag_index, metadata)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
