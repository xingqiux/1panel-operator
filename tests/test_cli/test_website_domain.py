from __future__ import annotations

import json

from typer.testing import CliRunner

runner = CliRunner()


def test_website_domain_help():
    from onepanel.cli.website_domain import app

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    output = result.output.lower()
    assert "list" in output
    assert "https" in output
    assert "nginx-conf" in output


def test_website_domain_list_help():
    from onepanel.cli.website_domain import app

    result = runner.invoke(app, ["list", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output
    assert "website_id" in result.output.lower() or "website id" in result.output.lower()


def test_website_domain_https_help():
    from onepanel.cli.website_domain import app

    result = runner.invoke(app, ["https", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output


def test_website_domain_nginx_conf_help():
    from onepanel.cli.website_domain import app

    result = runner.invoke(app, ["nginx-conf", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output


def test_website_help_includes_domain_subcommand():
    from onepanel.cli.website import app

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "domain" in result.output.lower()


def test_website_domain_list(monkeypatch):
    from onepanel.cli import website_domain
    from onepanel.cli.website import app as website_app

    class FakeClient:
        def __init__(self) -> None:
            self.requests: list[tuple[str, str, object, object, object]] = []

        def request(self, method, path, body=None, query=None, extra_headers=None):
            self.requests.append((method, path, body, query, extra_headers))
            return {
                "data": [
                    {"id": 1, "domain": "example.com", "port": 80, "ssl": False},
                    {"id": 2, "domain": "www.example.com", "port": 443, "ssl": True},
                ]
            }

        def normalize_response_payload(self, response):
            return response

    fake_client = FakeClient()
    monkeypatch.setattr(website_domain, "get_client", lambda ctx: fake_client)

    result = runner.invoke(website_app, ["domain", "list", "42"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("GET", "/websites/domains/42", None, None, None),
    ]
    assert json.loads(result.output) == {
        "count": 2,
        "items": [
            {"id": 1, "domain": "example.com", "port": 80, "ssl": False},
            {"id": 2, "domain": "www.example.com", "port": 443, "ssl": True},
        ],
    }


def test_website_domain_https(monkeypatch):
    from onepanel.cli import website_domain
    from onepanel.cli.website import app as website_app

    class FakeClient:
        def __init__(self) -> None:
            self.requests: list[tuple[str, str, object, object, object]] = []

        def request(self, method, path, body=None, query=None, extra_headers=None):
            self.requests.append((method, path, body, query, extra_headers))
            return {
                "data": {
                    "enable": True,
                    "hsts": False,
                    "httpConfig": "redirect",
                    "SSLProtocol": "TLSv1.2 TLSv1.3",
                }
            }

        def normalize_response_payload(self, response):
            return response

    fake_client = FakeClient()
    monkeypatch.setattr(website_domain, "get_client", lambda ctx: fake_client)

    result = runner.invoke(website_app, ["domain", "https", "42"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("GET", "/websites/42/https", None, None, None),
    ]
    assert json.loads(result.output) == {
        "enable": True,
        "hsts": False,
        "httpConfig": "redirect",
        "SSLProtocol": "TLSv1.2 TLSv1.3",
    }


def test_website_domain_nginx_conf(monkeypatch):
    from onepanel.cli import website_domain
    from onepanel.cli.website import app as website_app

    class FakeClient:
        def __init__(self) -> None:
            self.requests: list[tuple[str, str, object, object, object]] = []

        def request(self, method, path, body=None, query=None, extra_headers=None):
            self.requests.append((method, path, body, query, extra_headers))
            return {
                "data": "server {\n  listen 80;\n}",
            }

        def normalize_response_payload(self, response):
            return response

    fake_client = FakeClient()
    monkeypatch.setattr(website_domain, "get_client", lambda ctx: fake_client)

    result = runner.invoke(website_app, ["domain", "nginx-conf", "42", "proxy"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("GET", "/websites/42/config/proxy", None, None, None),
    ]
    assert json.loads(result.output) == "server {\n  listen 80;\n}"
