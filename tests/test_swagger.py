from __future__ import annotations

import time
from unittest.mock import MagicMock

import pytest

from onepanel.swagger import SwaggerCache, SwaggerOperation, SwaggerParser


SAMPLE_SPEC = {
    "paths": {
        "/api/v1/websites/list": {
            "get": {
                "summary": "List websites",
                "tags": ["Website"],
                "parameters": [],
                "responses": {},
            }
        },
        "/api/v1/apps/installed/list": {
            "get": {
                "summary": "List installed apps",
                "tags": ["App"],
                "parameters": [],
                "responses": {},
            }
        },
        "/api/v1/websites": {
            "post": {
                "summary": "Create website",
                "tags": ["Website"],
                "parameters": [
                    {
                        "in": "body",
                        "name": "body",
                        "schema": {"$ref": "#/definitions/request.WebsiteCreate"},
                    }
                ],
                "responses": {},
            }
        },
    },
    "definitions": {
        "request.WebsiteCreate": {
            "type": "object",
            "properties": {
                "primaryDomain": {"type": "string"},
                "type": {"type": "string"},
                "alias": {"type": "string"},
                "port": {"type": "integer"},
                "enable": {"type": "boolean"},
            },
        },
        "dto.SimpleItem": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
            },
        },
    },
}


@pytest.fixture
def mock_cache(tmp_path):
    mock_client = MagicMock()
    mock_client.config.base_url = "http://test-panel:8080"
    cache = SwaggerCache(client=mock_client, ttl_seconds=600, cache_dir=tmp_path)
    cache._swagger_spec = SAMPLE_SPEC
    return cache


@pytest.fixture
def parser(mock_cache):
    return SwaggerParser(mock_cache)


def test_swagger_operation_dataclass():
    op = SwaggerOperation(
        path="/api/v1/test",
        method="GET",
        summary="Test endpoint",
        tags=["Test"],
        body_schema_ref=None,
        path_params=["id"],
        query_params=["page"],
    )
    assert op.path == "/api/v1/test"
    assert op.method == "GET"
    assert op.summary == "Test endpoint"
    assert op.tags == ["Test"]
    assert op.path_params == ["id"]
    assert op.query_params == ["page"]


def test_list_operations_no_filter(parser: SwaggerParser):
    ops = parser.list_operations()
    assert len(ops) == 3
    paths = [op.path for op in ops]
    assert "/api/v1/apps/installed/list" in paths
    assert "/api/v1/websites/list" in paths
    assert "/api/v1/websites" in paths


def test_list_operations_match(parser: SwaggerParser):
    ops = parser.list_operations(match="website")
    assert len(ops) == 2
    for op in ops:
        assert "website" in op.path.lower() or "Website" in op.tags


def test_get_schema_by_name(parser: SwaggerParser):
    schema = parser.get_schema("request.WebsiteCreate")
    assert schema["type"] == "object"
    assert "primaryDomain" in schema["properties"]


def test_get_schema_by_ref(parser: SwaggerParser):
    schema = parser.get_schema("#/definitions/dto.SimpleItem")
    assert schema["type"] == "object"
    assert "id" in schema["properties"]


def test_build_schema_template(parser: SwaggerParser):
    template = parser.build_schema_template("request.WebsiteCreate")
    assert isinstance(template, dict)
    assert template["primaryDomain"] == ""
    assert template["port"] == 0
    assert template["enable"] is False


def test_cache_write_read(tmp_path):
    mock_client = MagicMock()
    mock_client.config.base_url = "http://test-panel:8080"
    cache = SwaggerCache(client=mock_client, ttl_seconds=600, cache_dir=tmp_path)
    cache._write_swagger_cache(SAMPLE_SPEC, "http://test-panel:8080/swagger/doc.json")
    cached = cache._read_swagger_cache()
    assert cached is not None
    assert cached["spec"] == SAMPLE_SPEC
    assert cached["source_url"] == "http://test-panel:8080/swagger/doc.json"


def test_cache_expired(tmp_path):
    mock_client = MagicMock()
    mock_client.config.base_url = "http://test-panel:8080"
    cache = SwaggerCache(client=mock_client, ttl_seconds=1, cache_dir=tmp_path)
    cache._write_swagger_cache(SAMPLE_SPEC, "http://test-panel:8080/swagger/doc.json")
    cache_file = cache._swagger_cache_file()
    old_time = time.time() - 10
    import os
    os.utime(cache_file, (old_time, old_time))
    cached = cache._read_swagger_cache()
    assert cached is None
