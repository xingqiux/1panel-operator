from __future__ import annotations

import json

from typer.testing import CliRunner

runner = CliRunner()


def _make_fake_client(normalized):
    class FakeClient:
        def __init__(self) -> None:
            self.requests: list[tuple[str, str, object, object, object]] = []

        def request(self, method, path, body=None, query=None, extra_headers=None):
            self.requests.append((method, path, body, query, extra_headers))
            return {"ok": True}

        def normalize_response_payload(self, response):
            return normalized

    return FakeClient()


def test_ai_help():
    from onepanel.cli.ai import app

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    output = result.output.lower()
    assert "gpu" in output
    assert "models" in output


def test_root_help_includes_ai_subcommand():
    from onepanel.cli import app as root_app

    result = runner.invoke(root_app, ["--help"])
    assert result.exit_code == 0
    assert "ai" in result.output.lower()


def test_ai_gpu_help():
    from onepanel.cli.ai import app

    result = runner.invoke(app, ["gpu", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output


def test_ai_models_help():
    from onepanel.cli.ai import app

    result = runner.invoke(app, ["models", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output


def test_ai_gpu(monkeypatch):
    from onepanel.cli import ai

    fake_client = _make_fake_client(
        {
            "data": {
                "enabled": True,
                "driverVersion": "550.54",
                "gpus": [{"name": "NVIDIA RTX 4090", "memory": "24G"}],
                "xpus": [],
            }
        }
    )
    monkeypatch.setattr(ai, "get_client", lambda ctx: fake_client)

    result = runner.invoke(ai.app, ["gpu"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("GET", "/ai/gpu", None, None, None),
    ]
    assert json.loads(result.output) == {
        "enabled": True,
        "driverVersion": "550.54",
        "gpus": [{"name": "NVIDIA RTX 4090", "memory": "24G"}],
        "xpus": [],
    }


def test_ai_models(monkeypatch):
    from onepanel.cli import ai

    fake_client = _make_fake_client(
        {
            "data": {
                "total": 2,
                "items": [
                    {
                        "id": 1,
                        "name": "llama3:8b",
                        "size": "4.7 GB",
                        "status": "loaded",
                        "createdAt": "2026-04-12T00:00:00Z",
                        "digest": "sha256:abc",
                    },
                    {
                        "id": 2,
                        "name": "qwen2.5",
                        "size": "5.1 GB",
                        "status": "available",
                        "createdAt": "2026-04-12T01:00:00Z",
                        "digest": "sha256:def",
                    },
                ],
            }
        }
    )
    monkeypatch.setattr(ai, "get_client", lambda ctx: fake_client)

    result = runner.invoke(ai.app, ["models"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("GET", "/ai/ollama/models", None, None, None),
    ]
    assert json.loads(result.output) == {
        "count": 2,
        "total": 2,
        "items": [
            {
                "id": 1,
                "name": "llama3:8b",
                "size": "4.7 GB",
                "status": "loaded",
                "createdAt": "2026-04-12T00:00:00Z",
            },
            {
                "id": 2,
                "name": "qwen2.5",
                "size": "5.1 GB",
                "status": "available",
                "createdAt": "2026-04-12T01:00:00Z",
            },
        ],
    }


def test_ai_models_raw(monkeypatch):
    from onepanel.cli import ai

    normalized = {
        "data": {"total": 1, "items": [{"id": 1, "name": "llama3"}]},
        "_meta": {"status_code": 200, "url": "https://example.com/api/v1/ai/ollama/models"},
    }
    fake_client = _make_fake_client(normalized)
    monkeypatch.setattr(ai, "get_client", lambda ctx: fake_client)

    result = runner.invoke(ai.app, ["models", "--raw"])
    assert result.exit_code == 0
    assert fake_client.requests == [
        ("GET", "/ai/ollama/models", None, None, None),
    ]
    assert json.loads(result.output) == normalized
