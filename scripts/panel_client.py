from __future__ import annotations

import copy
import hashlib
import json
import re
import ssl
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib import error, parse, request

from panel_auth import build_headers
from panel_config import PanelConfig, skill_root

SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}


class PanelAPIError(RuntimeError):
    def __init__(self, message: str, status_code: int | None = None, payload: Any | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.payload = payload


@dataclass
class SwaggerOperation:
    path: str
    method: str
    summary: str
    tags: List[str]
    body_schema_ref: str | None = None
    path_params: List[str] | None = None
    query_params: List[str] | None = None
    response_schema_ref: str | None = None


class PanelClient:
    def __init__(self, config: PanelConfig):
        self.config = config
        self._swagger_spec: Optional[Dict[str, Any]] = None
        self._swagger_url: Optional[str] = None
        self._ssl_context = None if config.verify_tls else ssl._create_unverified_context()
        self._cache_dir = skill_root() / ".cache"

    def _make_url(self, path_or_url: str, query: Optional[Dict[str, str]] = None) -> str:
        if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
            base = path_or_url
        elif path_or_url.startswith("/api/"):
            base = f"{self.config.base_url}{path_or_url}"
        elif path_or_url.startswith("/"):
            base = f"{self.config.base_url}/api/v1{path_or_url}"
        else:
            base = f"{self.config.base_url}/api/v1/{path_or_url}"

        if query:
            encoded = parse.urlencode(query)
            sep = "&" if "?" in base else "?"
            base = f"{base}{sep}{encoded}"
        return base

    def request(
        self,
        method: str,
        path_or_url: str,
        body: Any | None = None,
        query: Optional[Dict[str, str]] = None,
        extra_headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        method = method.upper()
        headers = build_headers(self.config.api_key)
        headers["Accept"] = "application/json"

        data = None
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"

        if extra_headers:
            headers.update(extra_headers)

        url = self._make_url(path_or_url, query=query)
        req = request.Request(url=url, data=data, headers=headers, method=method)
        try:
            with request.urlopen(req, timeout=self.config.timeout, context=self._ssl_context) as resp:
                raw = resp.read()
                return {
                    "url": url,
                    "status_code": resp.status,
                    "headers": dict(resp.headers.items()),
                    "body": self._decode_payload(raw, resp.headers.get("Content-Type", "")),
                }
        except error.HTTPError as exc:
            raw = exc.read()
            payload = self._decode_payload(raw, exc.headers.get("Content-Type", ""))
            raise PanelAPIError(
                f"1Panel API returned HTTP {exc.code} for {method} {url}",
                status_code=exc.code,
                payload=payload,
            ) from exc
        except error.URLError as exc:
            raise PanelAPIError(f"Failed to reach 1Panel API at {url}: {exc.reason}") from exc

    def ping(self) -> Dict[str, Any]:
        return self.request("GET", "/websites/list")

    def swagger_url(self) -> str:
        if self._swagger_url:
            return self._swagger_url

        cached = self._read_swagger_cache()
        if cached and cached.get("source_url"):
            self._swagger_url = str(cached["source_url"])
            return self._swagger_url

        candidates = [
            f"{self.config.base_url}/1panel/swagger/doc.json",
            f"{self.config.base_url}/swagger/doc.json",
            f"{self.config.base_url}/v3/api-docs",
            f"{self.config.base_url}/openapi.json",
        ]

        index_url = f"{self.config.base_url}/1panel/swagger/index.html"
        try:
            index_resp = self.request("GET", index_url)
            index_text = index_resp["body"].get("text", "")
            match = re.search(r'url:\s*"([^"]+)"', index_text)
            if match:
                url = match.group(1)
                if not url.startswith("http"):
                    url = parse.urljoin(index_url, url)
                candidates.insert(0, url)
        except PanelAPIError:
            pass

        seen = set()
        for candidate in candidates:
            if candidate in seen:
                continue
            seen.add(candidate)
            try:
                self.request("GET", candidate)
                self._swagger_url = candidate
                return candidate
            except PanelAPIError:
                continue

        raise PanelAPIError("Could not resolve a working Swagger/OpenAPI JSON URL.")

    def swagger_spec(self) -> Dict[str, Any]:
        if self._swagger_spec is not None:
            return self._swagger_spec

        cached = self._read_swagger_cache()
        if cached and isinstance(cached.get("spec"), dict):
            self._swagger_spec = cached["spec"]
            self._swagger_url = str(cached.get("source_url", self._swagger_url or ""))
            return self._swagger_spec

        response = self.request("GET", self.swagger_url())
        body = response["body"]
        json_obj = body.get("json")
        if not isinstance(json_obj, dict):
            raise PanelAPIError("Swagger payload is not a JSON object.", payload=body)
        self._swagger_spec = json_obj
        self._write_swagger_cache(json_obj, self.swagger_url())
        return json_obj

    def list_operations(self, match: str | None = None, tag: str | None = None) -> List[SwaggerOperation]:
        spec = self.swagger_spec()
        operations: List[SwaggerOperation] = []
        needle = (match or "").lower()
        tag_needle = (tag or "").lower()

        for path, methods in spec.get("paths", {}).items():
            for method, operation in methods.items():
                summary = operation.get("summary", "")
                tags = operation.get("tags", [])
                body_schema_ref = None
                path_params: List[str] = []
                query_params: List[str] = []
                for param in operation.get("parameters", []):
                    if param.get("in") == "body":
                        body_schema_ref = param.get("schema", {}).get("$ref")
                    elif param.get("in") == "path":
                        path_params.append(param.get("name", ""))
                    elif param.get("in") == "query":
                        query_params.append(param.get("name", ""))

                response_schema_ref = None
                for _, response in operation.get("responses", {}).items():
                    schema = response.get("schema", {})
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

    def list_tags(self) -> List[Dict[str, Any]]:
        counts: Dict[str, int] = {}
        for operation in self.list_operations():
            for tag in operation.tags or ["(untagged)"]:
                counts[tag] = counts.get(tag, 0) + 1
        return [{"tag": tag, "count": counts[tag]} for tag in sorted(counts, key=lambda item: (-counts[item], item.lower()))]

    def get_operation(self, path: str, method: str | None = None) -> SwaggerOperation:
        wanted_method = method.upper() if method else None
        candidates = [op for op in self.list_operations() if op.path == path and (wanted_method is None or op.method == wanted_method)]
        if not candidates:
            raise PanelAPIError(f"No Swagger operation found for path={path} method={wanted_method or '*'}")
        if len(candidates) > 1 and wanted_method is None:
            methods = ", ".join(op.method for op in candidates)
            raise PanelAPIError(f"Multiple operations match {path}. Specify a method. Candidates: {methods}")
        return candidates[0]

    def list_schema_names(self, match: str | None = None) -> List[str]:
        definitions = self.swagger_spec().get("definitions", {})
        names = sorted(definitions.keys())
        if not match:
            return names
        needle = match.lower()
        return [name for name in names if needle in name.lower()]

    def get_schema(self, name_or_ref: str) -> Dict[str, Any]:
        name = name_or_ref
        if name.startswith("#/definitions/"):
            name = name.split("/", 2)[-1]
        schema = self.swagger_spec().get("definitions", {}).get(name)
        if not isinstance(schema, dict):
            raise PanelAPIError(f"Swagger definition not found: {name_or_ref}")
        return schema

    def build_schema_template(self, name_or_ref: str, max_depth: int = 4) -> Any:
        return self._schema_to_template({"$ref": self._normalize_ref(name_or_ref)}, depth=0, max_depth=max_depth)

    def build_operation_template(self, path: str, method: str) -> Dict[str, Any]:
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

    def _schema_to_template(self, schema: Dict[str, Any], depth: int, max_depth: int) -> Any:
        if depth > max_depth:
            return "<max-depth>"

        if "$ref" in schema:
            resolved = copy.deepcopy(self.get_schema(schema["$ref"]))
            return self._schema_to_template(resolved, depth + 1, max_depth)

        if "allOf" in schema:
            merged: Dict[str, Any] = {"type": "object", "properties": {}, "required": []}
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
            required = set(schema.get("required", []))
            result: Dict[str, Any] = {}
            for key, value in properties.items():
                rendered = self._schema_to_template(value, depth + 1, max_depth)
                if key in required:
                    result[key] = rendered
                else:
                    result[key] = rendered
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

    def plan(self, method: str, path_or_url: str, body: Any | None = None, query: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        method = method.upper()
        return {
            "method": method,
            "url": self._make_url(path_or_url, query=query),
            "write_operation": method not in SAFE_METHODS,
            "body": body,
            "query": query or {},
        }

    def normalize_response_payload(self, response: Dict[str, Any]) -> Dict[str, Any]:
        body = response["body"]
        meta = {
            "status_code": response["status_code"],
            "url": response["url"],
        }
        json_obj = body.get("json")
        if isinstance(json_obj, dict) and {"code", "data", "message"}.issubset(json_obj.keys()):
            return {
                "code": json_obj.get("code"),
                "message": json_obj.get("message"),
                "data": json_obj.get("data"),
                "_meta": meta,
            }
        return {
            "data": json_obj if json_obj is not None else body.get("text"),
            "_meta": meta,
        }

    def cache_info(self) -> Dict[str, Any]:
        cache_file = self._swagger_cache_file()
        exists = cache_file.exists()
        info: Dict[str, Any] = {
            "enabled": self.config.swagger_cache_ttl_seconds > 0,
            "path": str(cache_file),
            "exists": exists,
            "ttl_seconds": self.config.swagger_cache_ttl_seconds,
        }
        if exists:
            stat = cache_file.stat()
            info["age_seconds"] = round(time.time() - stat.st_mtime, 3)
        return info

    @staticmethod
    def _decode_payload(raw: bytes, content_type: str) -> Dict[str, Any]:
        text = raw.decode("utf-8", errors="replace")
        normalized = text.strip()
        payload: Dict[str, Any] = {"text": normalized}

        json_text = normalized
        if normalized.startswith("<!DOCTYPE html>") and "\n{" in normalized:
            json_text = normalized[normalized.rfind("\n{") + 1 :]
        elif normalized.startswith("<!DOCTYPE html>") and "{" in normalized:
            json_text = normalized[normalized.rfind("{") :]

        if "json" in content_type.lower() or json_text.startswith("{") or json_text.startswith("["):
            try:
                payload["json"] = json.loads(json_text)
            except json.JSONDecodeError:
                pass
        return payload

    def _swagger_cache_file(self) -> Path:
        hashed = hashlib.sha256(self.config.base_url.encode("utf-8")).hexdigest()[:16]
        return self._cache_dir / f"swagger-{hashed}.json"

    def _read_swagger_cache(self) -> Optional[Dict[str, Any]]:
        if self.config.swagger_cache_ttl_seconds <= 0:
            return None
        cache_file = self._swagger_cache_file()
        if not cache_file.exists():
            return None
        age = time.time() - cache_file.stat().st_mtime
        if age > self.config.swagger_cache_ttl_seconds:
            return None
        try:
            return json.loads(cache_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return None

    def _write_swagger_cache(self, spec: Dict[str, Any], source_url: str) -> None:
        if self.config.swagger_cache_ttl_seconds <= 0:
            return
        self._cache_dir.mkdir(parents=True, exist_ok=True)
        cache_file = self._swagger_cache_file()
        payload = {
            "source_url": source_url,
            "spec": spec,
        }
        cache_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
