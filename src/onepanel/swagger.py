from __future__ import annotations

import copy
import hashlib
import json
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any
from urllib.parse import urljoin

from onepanel.config import skill_root
from onepanel.models import PanelAPIError

if TYPE_CHECKING:
    from onepanel.client import PanelClient


@dataclass
class SwaggerOperation:
    path: str
    method: str
    summary: str
    tags: list[str]
    body_schema_ref: str | None = None
    path_params: list[str] = field(default_factory=list)
    query_params: list[str] = field(default_factory=list)
    response_schema_ref: str | None = None


class SwaggerCache:
    def __init__(self, client: PanelClient, ttl_seconds: int, cache_dir: Path | None = None) -> None:
        self._client = client
        self._ttl_seconds = ttl_seconds
        self._cache_dir = cache_dir or (skill_root() / ".cache")
        self._swagger_spec: dict[str, Any] | None = None
        self._swagger_url: str | None = None

    def swagger_url(self) -> str:
        if self._swagger_url:
            return self._swagger_url

        cached = self._read_swagger_cache()
        if cached and cached.get("source_url"):
            self._swagger_url = str(cached["source_url"])
            return self._swagger_url

        base_url = self._client.config.base_url
        candidates = [
            f"{base_url}/1panel/swagger/doc.json",
            f"{base_url}/swagger/doc.json",
            f"{base_url}/v3/api-docs",
            f"{base_url}/openapi.json",
        ]

        index_url = f"{base_url}/1panel/swagger/index.html"
        try:
            index_resp = self._client.request("GET", index_url)
            index_text = index_resp["body"].get("text", "")
            match = re.search(r'url:\s*"([^"]+)"', index_text)
            if match:
                url = match.group(1)
                if not url.startswith("http"):
                    url = urljoin(index_url, url)
                candidates.insert(0, url)
        except PanelAPIError:
            pass

        seen: set[str] = set()
        for candidate in candidates:
            if candidate in seen:
                continue
            seen.add(candidate)
            try:
                self._client.request("GET", candidate)
                self._swagger_url = candidate
                return candidate
            except PanelAPIError:
                continue

        raise PanelAPIError("Could not resolve a working Swagger/OpenAPI JSON URL.")

    def swagger_spec(self) -> dict[str, Any]:
        if self._swagger_spec is not None:
            return self._swagger_spec

        cached = self._read_swagger_cache()
        if cached and isinstance(cached.get("spec"), dict):
            self._swagger_spec = cached["spec"]
            self._swagger_url = str(cached.get("source_url", self._swagger_url or ""))
            return self._swagger_spec

        response = self._client.request("GET", self.swagger_url())
        body = response["body"]
        json_obj = body.get("json")
        if not isinstance(json_obj, dict):
            raise PanelAPIError("Swagger payload is not a JSON object.", payload=body)
        self._swagger_spec = json_obj
        self._write_swagger_cache(json_obj, self.swagger_url())
        return json_obj

    def cache_info(self) -> dict[str, Any]:
        cache_file = self._swagger_cache_file()
        exists = cache_file.exists()
        info: dict[str, Any] = {
            "enabled": self._ttl_seconds > 0,
            "path": str(cache_file),
            "exists": exists,
            "ttl_seconds": self._ttl_seconds,
        }
        if exists:
            stat = cache_file.stat()
            info["age_seconds"] = round(time.time() - stat.st_mtime, 3)
        return info

    def _swagger_cache_file(self) -> Path:
        hashed = hashlib.sha256(self._client.config.base_url.encode("utf-8")).hexdigest()[:16]
        return self._cache_dir / f"swagger-{hashed}.json"

    def _read_swagger_cache(self) -> dict[str, Any] | None:
        if self._ttl_seconds <= 0:
            return None
        cache_file = self._swagger_cache_file()
        if not cache_file.exists():
            return None
        age = time.time() - cache_file.stat().st_mtime
        if age > self._ttl_seconds:
            return None
        try:
            return json.loads(cache_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return None

    def _write_swagger_cache(self, spec: dict[str, Any], source_url: str) -> None:
        if self._ttl_seconds <= 0:
            return
        self._cache_dir.mkdir(parents=True, exist_ok=True)
        cache_file = self._swagger_cache_file()
        payload = {
            "source_url": source_url,
            "spec": spec,
        }
        cache_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


class SwaggerParser:
    def __init__(self, cache: SwaggerCache) -> None:
        self._cache = cache

    def list_operations(self, match: str | None = None, tag: str | None = None) -> list[SwaggerOperation]:
        spec = self._cache.swagger_spec()
        operations: list[SwaggerOperation] = []
        needle = (match or "").lower()
        tag_needle = (tag or "").lower()

        for path, methods in spec.get("paths", {}).items():
            for method, operation in methods.items():
                summary = operation.get("summary", "")
                tags = operation.get("tags", [])

                body_schema_ref = None
                path_params: list[str] = []
                query_params: list[str] = []
                for param in operation.get("parameters", []):
                    if param.get("in") == "body":
                        body_schema_ref = param.get("schema", {}).get("$ref")
                    elif param.get("in") == "path":
                        path_params.append(param.get("name", ""))
                    elif param.get("in") == "query":
                        query_params.append(param.get("name", ""))

                response_schema_ref = None
                for _, resp in operation.get("responses", {}).items():
                    schema = resp.get("schema", {})
                    if "$ref" in schema:
                        response_schema_ref = schema["$ref"]
                        break
                    items = schema.get("items", {})
                    if "$ref" in items:
                        response_schema_ref = items["$ref"]
                        break

                if needle:
                    haystack = " ".join([path, summary, " ".join(tags)]).lower()
                    if needle not in haystack:
                        continue
                if tag_needle and tag_needle not in " ".join(tags).lower():
                    continue

                operations.append(
                    SwaggerOperation(
                        path=path,
                        method=method.upper(),
                        summary=summary,
                        tags=list(tags),
                        body_schema_ref=body_schema_ref,
                        path_params=path_params,
                        query_params=query_params,
                        response_schema_ref=response_schema_ref,
                    )
                )

        operations.sort(key=lambda item: (item.path, item.method))
        return operations

    def list_tags(self) -> list[dict[str, Any]]:
        counts: dict[str, int] = {}
        for operation in self.list_operations():
            for tag in operation.tags or ["(untagged)"]:
                counts[tag] = counts.get(tag, 0) + 1
        return [
            {"tag": tag, "count": counts[tag]}
            for tag in sorted(counts, key=lambda item: (-counts[item], item.lower()))
        ]

    def get_operation(self, path: str, method: str | None = None) -> SwaggerOperation:
        wanted_method = method.upper() if method else None
        candidates = [
            op for op in self.list_operations()
            if op.path == path and (wanted_method is None or op.method == wanted_method)
        ]
        if not candidates:
            raise PanelAPIError(f"No Swagger operation found for path={path} method={wanted_method or '*'}")
        if len(candidates) > 1 and wanted_method is None:
            methods = ", ".join(op.method for op in candidates)
            raise PanelAPIError(f"Multiple operations match {path}. Specify a method. Candidates: {methods}")
        return candidates[0]

    def list_schema_names(self, match: str | None = None) -> list[str]:
        definitions = self._cache.swagger_spec().get("definitions", {})
        names = sorted(definitions.keys())
        if not match:
            return names
        needle = match.lower()
        return [name for name in names if needle in name.lower()]

    def get_schema(self, name_or_ref: str) -> dict[str, Any]:
        name = name_or_ref
        if name.startswith("#/definitions/"):
            name = name.split("/", 2)[-1]
        schema = self._cache.swagger_spec().get("definitions", {}).get(name)
        if not isinstance(schema, dict):
            raise PanelAPIError(f"Swagger definition not found: {name_or_ref}")
        return schema

    def build_schema_template(self, name_or_ref: str, max_depth: int = 4) -> Any:
        return self._schema_to_template({"$ref": self._normalize_ref(name_or_ref)}, depth=0, max_depth=max_depth)

    def build_operation_template(self, path: str, method: str) -> dict[str, Any]:
        operation = self.get_operation(path, method)
        body_template = None
        if operation.body_schema_ref:
            body_template = self.build_schema_template(operation.body_schema_ref)
        return {
            "method": operation.method,
            "path": operation.path,
            "summary": operation.summary,
            "tags": operation.tags,
            "path_params": operation.path_params or [],
            "query_params": operation.query_params or [],
            "body_schema_ref": operation.body_schema_ref,
            "response_schema_ref": operation.response_schema_ref,
            "body_template": body_template,
        }

    def _schema_to_template(self, schema: dict[str, Any], depth: int, max_depth: int) -> Any:
        if depth > max_depth:
            return "<max-depth>"

        if "$ref" in schema:
            resolved = copy.deepcopy(self.get_schema(schema["$ref"]))
            return self._schema_to_template(resolved, depth + 1, max_depth)

        if "allOf" in schema:
            merged: dict[str, Any] = {"type": "object", "properties": {}, "required": []}
            for item in schema["allOf"]:
                value = self._schema_to_template(item, depth + 1, max_depth)
                if isinstance(value, dict):
                    merged["properties"].update(value)
            return merged["properties"]

        schema_type = schema.get("type")
        if not schema_type and "properties" in schema:
            schema_type = "object"

        if schema_type == "object":
            properties = schema.get("properties", {})
            result: dict[str, Any] = {}
            for key, value in properties.items():
                result[key] = self._schema_to_template(value, depth + 1, max_depth)
            return result

        if schema_type == "array":
            return [self._schema_to_template(schema.get("items", {}), depth + 1, max_depth)]

        if "enum" in schema:
            return schema["enum"][0] if schema["enum"] else "<enum>"

        if schema_type == "string":
            return ""
        if schema_type == "integer":
            return 0
        if schema_type == "number":
            return 0
        if schema_type == "boolean":
            return False

        return None

    @staticmethod
    def _normalize_ref(name_or_ref: str) -> str:
        if name_or_ref.startswith("#/definitions/"):
            return name_or_ref
        return f"#/definitions/{name_or_ref}"
