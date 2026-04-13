from __future__ import annotations

from typer.testing import CliRunner

runner = CliRunner()


def test_website_ca_help():
    from onepanel.cli.website_ca import app

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    output = result.output.lower()
    assert "list" in output
    assert "show" in output


def test_website_ca_list_help():
    from onepanel.cli.website_ca import app

    result = runner.invoke(app, ["list", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output
    assert "--page" in result.output
    assert "--page-size" in result.output


def test_website_ca_show_help():
    from onepanel.cli.website_ca import app

    result = runner.invoke(app, ["show", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output


def test_website_help_includes_ca_subcommand():
    from onepanel.cli.website import app

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "ca" in result.output.lower()

