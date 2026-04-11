from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class PanelConfigError(RuntimeError):
    pass


def skill_root() -> Path:
    return Path(__file__).resolve().parents[2]


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


class PanelConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ONEPANEL_")

    base_url: str = ""
    api_key: str = ""
    timeout: int = 20
    verify_tls: bool = True
    swagger_cache_ttl_seconds: int = 600

    @property
    def masked_api_key(self) -> str:
        if len(self.api_key) <= 8:
            return "*" * len(self.api_key)
        return f"{self.api_key[:4]}...{self.api_key[-4:]}"

    @model_validator(mode="before")
    @classmethod
    def _fill_from_legacy_env_and_json(cls, values: dict[str, Any]) -> dict[str, Any]:
        local_path = skill_root() / "config" / "local.json"
        local_data = _load_json_config(local_path)

        legacy_map = {
            "base_url": "1PANEL_BASE_URL",
            "api_key": "1PANEL_API_KEY",
            "timeout": "1PANEL_TIMEOUT",
            "verify_tls": "1PANEL_VERIFY_TLS",
            "swagger_cache_ttl_seconds": "1PANEL_SWAGGER_CACHE_TTL",
        }

        for field, env_var in legacy_map.items():
            if values.get(field):
                continue
            env_val = os.getenv(env_var)
            if env_val is not None:
                if field == "verify_tls":
                    values[field] = _parse_bool(env_val, default=True)
                elif field in ("timeout", "swagger_cache_ttl_seconds"):
                    values[field] = int(env_val)
                else:
                    values[field] = env_val
            elif field in local_data:
                val = local_data[field]
                if field == "verify_tls":
                    values[field] = _parse_bool(val, default=True)
                else:
                    values[field] = val

        if values.get("base_url"):
            values["base_url"] = str(values["base_url"]).rstrip("/")

        if not values.get("base_url"):
            raise PanelConfigError("Missing 1Panel base URL. Set ONEPANEL_BASE_URL, 1PANEL_BASE_URL, or config/local.json.")
        if not values.get("api_key"):
            raise PanelConfigError("Missing 1Panel API key. Set ONEPANEL_API_KEY, 1PANEL_API_KEY, or config/local.json.")

        return values
