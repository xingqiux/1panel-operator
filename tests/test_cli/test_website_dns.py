from __future__ import annotations

import json

from typer.testing import CliRunner

runner = CliRunner()


def test_website_dns_help():
    from onepanel.cli.website_dns import app

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    output = result.output.lower()
    assert "list" in output


def test_website_dns_list_help():
    from onepanel.cli.website_dns import app

    result = runner.invoke(app, ["list", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output
    assert "--page" in result.output
    assert "--page-size" in result.output


def test_website_help_includes_dns_subcommand():
    from onepanel.cli.website import app

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "dns" in result.output.lower()


def test_website_dns_list(monkeypatch):
    from onepanel.cli import website_dns
    from onepanel.cli.website import app as website_app

    class FakeClient:
        def __init__(self) -> None:
            self.requests: list[tuple[str, str, dict[str, int], dict[str, str] | None, dict[str, str] | None]] = []

        def request(
            self,
            method: str,
            path: str,
            body=None,
            query=None,
            extra_headers=None,
        ):
            self.requests.append((method, path, body, query, extra_headers))
            return {"ok": True}

        def normalize_response_payload(self, response):
            return {
                "data": {
                    "total": 2,
                    "items": [
                        {"id": 1, "name": "Cloudflare", "type": "cloudflare"},
                        {"id": 2, "name": "Route53", "type": "route53"},
                    ],
                }
            }

    fake_client = FakeClient()
    monkeypatch.setattr(website_dns, "get_client", lambda ctx: fake_client)

    result = runner.invoke(website_app, ["dns", "list", "--page", "3", "--page-size", "50"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("POST", "/websites/dns/search", {"page": 3, "pageSize": 50}, None, None),
    ]
    assert json.loads(result.output) == {
        "count": 2,
        "items": [
            {"id": 1, "name": "Cloudflare", "type": "cloudflare"},
            {"id": 2, "name": "Route53", "type": "route53"},
        ],
        "total": 2,
    }
