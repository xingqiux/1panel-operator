from __future__ import annotations

from typer.testing import CliRunner

runner = CliRunner()


def test_container_volume_help():
    from onepanel.cli.container_volume import app

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    output = result.output.lower()
    assert "list" in output
    assert "options" in output


def test_container_volume_list_help():
    from onepanel.cli.container_volume import app

    result = runner.invoke(app, ["list", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output
    assert "--page" in result.output
    assert "--page-size" in result.output


def test_container_volume_options_help():
    from onepanel.cli.container_volume import app

    result = runner.invoke(app, ["options", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output


def test_container_help_includes_volume_subcommand():
    from onepanel.cli.container import app

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "volume" in result.output.lower()
