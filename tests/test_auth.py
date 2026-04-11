from __future__ import annotations

import hashlib

from onepanel.auth import build_headers, build_token


def test_build_token_deterministic():
    api_key = "my-secret-key"
    timestamp = "1700000000"
    token, ts = build_token(api_key, timestamp=timestamp)
    expected_raw = f"1panel{api_key}{timestamp}".encode("utf-8")
    expected = hashlib.md5(expected_raw).hexdigest()
    assert token == expected
    assert ts == timestamp


def test_build_token_uses_current_time():
    token, ts = build_token("some-key")
    assert ts.isdigit()
    assert len(token) == 32


def test_build_headers_keys():
    headers = build_headers("some-key", timestamp="1700000000")
    assert set(headers.keys()) == {"1Panel-Token", "1Panel-Timestamp"}


def test_build_headers_token_matches():
    api_key = "another-key"
    timestamp = "1700000000"
    headers = build_headers(api_key, timestamp=timestamp)
    expected_token, _ = build_token(api_key, timestamp=timestamp)
    assert headers["1Panel-Token"] == expected_token
    assert headers["1Panel-Timestamp"] == timestamp
