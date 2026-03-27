from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path


class PanelConfigError(RuntimeError):
    pass


@dataclass
class PanelConfig:
    base_url: str
    api_key: str
    timeout: int = 20
    verify_tls: bool = True
    swagger_cache_ttl_seconds: int = 600
    source: str = "unknown"

    @property
    def masked_api_key(self) -> str:
        if len(self.api_key) <= 8:
            return "*" * len(self.api_key)
        return f"{self.api_key[:4]}...{self.api_key[-4:]}"


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _parse_bool(raw: str | bool | None, default: bool = True) -> bool:
    if raw is None:
        return default
    if isinstance(raw, bool):
        return raw
    return raw.strip().lower() not in {"0", "false", "no", "off"}


def _load_json_config(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise PanelConfigError(f"Invalid JSON config: {path}") from exc


def load_config() -> PanelConfig:
    local_path = skill_root() / "config" / "local.json"
    local_data = _load_json_config(local_path)

    base_url = os.getenv("1PANEL_BASE_URL") or local_data.get("base_url")
    api_key = os.getenv("1PANEL_API_KEY") or local_data.get("api_key")
    timeout_raw = os.getenv("1PANEL_TIMEOUT") or local_data.get("timeout", 20)
    verify_raw = os.getenv("1PANEL_VERIFY_TLS")
    if verify_raw is None:
        verify_raw = local_data.get("verify_tls", True)
    swagger_cache_ttl_raw = os.getenv("1PANEL_SWAGGER_CACHE_TTL") or local_data.get("swagger_cache_ttl_seconds", 600)

    if not base_url:
        raise PanelConfigError("Missing 1Panel base URL. Set 1PANEL_BASE_URL or config/local.json.")
    if not api_key:
        raise PanelConfigError("Missing 1Panel API key. Set 1PANEL_API_KEY or config/local.json.")

    source = "environment"
    if not os.getenv("1PANEL_BASE_URL") or not os.getenv("1PANEL_API_KEY"):
        source = "config/local.json"

    return PanelConfig(
        base_url=str(base_url).rstrip("/"),
        api_key=str(api_key),
        timeout=int(timeout_raw),
        verify_tls=_parse_bool(verify_raw, default=True),
        swagger_cache_ttl_seconds=max(0, int(swagger_cache_ttl_raw)),
        source=source,
    )
