from __future__ import annotations

import hashlib
import time


def build_token(api_key: str, timestamp: str | None = None) -> tuple[str, str]:
    value = timestamp or str(int(time.time()))
    raw = f"1panel{api_key}{value}".encode("utf-8")
    token = hashlib.md5(raw).hexdigest()
    return token, value


def build_headers(api_key: str, timestamp: str | None = None) -> dict[str, str]:
    token, value = build_token(api_key, timestamp=timestamp)
    return {
        "1Panel-Token": token,
        "1Panel-Timestamp": value,
    }
