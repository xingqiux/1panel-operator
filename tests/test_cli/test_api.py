from __future__ import annotations

from typer.testing import CliRunner

runner = CliRunner()


def test_api_discover_help():
    from onepanel.cli.api import app

    result = runner.invoke(app, ["discover", "--help"])
    assert result.exit_code == 0
    assert "discover" in result.output.lower() or "help" in result.output.lower()


def test_api_schema_help():
    from onepanel.cli.api import app

    result = runner.invoke(app, ["schema", "--help"])
    assert result.exit_code == 0
    assert "list" in result.output.lower()
    assert "show" in result.output.lower()


def test_api_schema_show_help():
    from onepanel.cli.api import app

    result = runner.invoke(app, ["schema", "show", "--help"])
    assert result.exit_code == 0
    assert "definition" in result.output.lower() or "schema" in result.output.lower()


def test_api_template_help():
    from onepanel.cli.api import app

    result = runner.invoke(app, ["template", "--help"])
    assert result.exit_code == 0
    assert "method" in result.output.lower()
    assert "path" in result.output.lower()


def test_api_call_help():
    from onepanel.cli.api import app

    result = runner.invoke(app, ["call", "--help"])
    assert result.exit_code == 0
    assert "method" in result.output.lower() or "path" in result.output.lower()
