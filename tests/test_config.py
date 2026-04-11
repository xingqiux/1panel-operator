from __future__ import annotations


from onepanel.config import PanelConfig


def test_config_from_env(monkeypatch):
    monkeypatch.setenv("ONEPANEL_BASE_URL", "http://panel.local:9090")
    monkeypatch.setenv("ONEPANEL_API_KEY", "env-key-abcdef1234")
    config = PanelConfig()
    assert config.base_url == "http://panel.local:9090"
    assert config.api_key == "env-key-abcdef1234"


def test_config_masked_api_key_short(monkeypatch):
    monkeypatch.setenv("ONEPANEL_BASE_URL", "http://panel.local")
    monkeypatch.setenv("ONEPANEL_API_KEY", "short")
    config = PanelConfig()
    assert config.masked_api_key == "*****"


def test_config_masked_api_key_long(monkeypatch):
    monkeypatch.setenv("ONEPANEL_BASE_URL", "http://panel.local")
    monkeypatch.setenv("ONEPANEL_API_KEY", "abcdefghijklmnop")
    config = PanelConfig()
    assert config.masked_api_key == "abcd...mnop"


def test_config_backward_compat_1panel_prefix(monkeypatch):
    monkeypatch.setenv("1PANEL_BASE_URL", "http://legacy.local:8080")
    monkeypatch.setenv("1PANEL_API_KEY", "legacy-key-12345678")
    monkeypatch.delenv("ONEPANEL_BASE_URL", raising=False)
    monkeypatch.delenv("ONEPANEL_API_KEY", raising=False)
    config = PanelConfig()
    assert config.base_url == "http://legacy.local:8080"
    assert config.api_key == "legacy-key-12345678"


def test_config_defaults(monkeypatch):
    monkeypatch.setenv("ONEPANEL_BASE_URL", "http://panel.local")
    monkeypatch.setenv("ONEPANEL_API_KEY", "some-key")
    config = PanelConfig()
    assert config.timeout == 20
    assert config.verify_tls is True
    assert config.swagger_cache_ttl_seconds == 600
