from __future__ import annotations

from typer.testing import CliRunner

runner = CliRunner()


def test_website_list_help():
    from onepanel.cli.website import app

    result = runner.invoke(app, ["list", "--help"])
    assert result.exit_code == 0
    assert "list" in result.output.lower() or "help" in result.output.lower()


def test_website_overview_help():
    from onepanel.cli.website import app

    result = runner.invoke(app, ["overview", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output or "--help" in result.output
