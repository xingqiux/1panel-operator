from __future__ import annotations

from typer.testing import CliRunner

runner = CliRunner()


def test_website_acme_help():
    from onepanel.cli.website_acme import app

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "list" in result.output.lower()


def test_website_acme_list_help():
    from onepanel.cli.website_acme import app

    result = runner.invoke(app, ["list", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output
    assert "--page" in result.output
    assert "--page-size" in result.output


def test_website_help_includes_acme_subcommand():
    from onepanel.cli.website import app

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "acme" in result.output.lower()

