from __future__ import annotations

import json
from typing import Any
from urllib.parse import urlencode

import httpx

from onepanel.auth import build_headers
from onepanel.config import PanelConfig
from onepanel.models import PanelAPIError
from onepanel.swagger import SwaggerCache
from onepanel.types import HTTPResponse, NormalizedResponse

SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}


class PanelClient:
    def __init__(self, config: PanelConfig) -> None:
        self.config = config
        self._http = httpx.Client(
            base_url=config.base_url,
            timeout=config.timeout,
            verify=config.verify_tls,
        )
        self._swagger_cache = SwaggerCache(client=self, ttl_seconds=config.swagger_cache_ttl_seconds)

    def _make_url(self, path_or_url: str, query: dict[str, str] | None = None) -> str:
        if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
            base = path_or_url
        elif path_or_url.startswith("/api/"):
            base = f"{self.config.base_url}{path_or_url}"
        elif path_or_url.startswith("/"):
            base = f"{self.config.base_url}/api/v1{path_or_url}"
        else:
            base = f"{self.config.base_url}/api/v1/{path_or_url}"

        if query:
            encoded = urlencode(query)
            sep = "&" if "?" in base else "?"
            base = f"{base}{sep}{encoded}"
        return base

    def request(
        self,
        method: str,
        path_or_url: str,
        body: Any | None = None,
        query: dict[str, str] | None = None,
        extra_headers: dict[str, str] | None = None,
    ) -> HTTPResponse:
        method = method.upper()
        headers = build_headers(self.config.api_key)
        headers["Accept"] = "application/json"

        content: bytes | None = None
        if body is not None:
            content = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"

        if extra_headers:
            headers.update(extra_headers)

        url = self._make_url(path_or_url, query=query)

        try:
            resp = self._http.request(method, url, content=content, headers=headers)
            resp.raise_for_status()
            return {
                "url": url,
                "status_code": resp.status_code,
                "headers": dict(resp.headers),
                "body": self._decode_payload(resp.content, resp.headers.get("content-type", "")),
            }
        except httpx.HTTPStatusError as exc:
            payload = self._decode_payload(exc.response.content, exc.response.headers.get("content-type", ""))
            raise PanelAPIError(
                f"1Panel API returned HTTP {exc.response.status_code} for {method} {url}",
                status_code=exc.response.status_code,
                payload=payload,
            ) from exc
        except httpx.RequestError as exc:
            raise PanelAPIError(f"Failed to reach 1Panel API at {url}: {exc}") from exc

    def plan(
        self,
        method: str,
        path_or_url: str,
        body: Any | None = None,
        query: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        method = method.upper()
        return {
            "method": method,
            "url": self._make_url(path_or_url, query=query),
            "write_operation": method not in SAFE_METHODS,
            "body": body,
            "query": query or {},
        }

    def ping(self) -> dict[str, Any]:
        return self.request("GET", "/websites/list")

    def normalize_response_payload(self, response: HTTPResponse) -> NormalizedResponse:
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

    def cache_info(self) -> dict[str, Any]:
        return self._swagger_cache.cache_info()

    @staticmethod
    def _decode_payload(raw: bytes, content_type: str) -> dict[str, Any]:
        text = raw.decode("utf-8", errors="replace")
        normalized = text.strip()
        payload: dict[str, Any] = {"text": normalized}

        json_text = normalized
        if normalized.startswith("<!DOCTYPE html>") and "\n{" in normalized:
            json_text = normalized[normalized.rfind("\n{") + 1:]
        elif normalized.startswith("<!DOCTYPE html>") and "{" in normalized:
            json_text = normalized[normalized.rfind("{"):]

        if "json" in content_type.lower() or json_text.startswith("{") or json_text.startswith("["):
            try:
                payload["json"] = json.loads(json_text)
            except json.JSONDecodeError:
                pass
        return payload
