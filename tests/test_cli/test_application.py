from __future__ import annotations

from typer.testing import CliRunner

runner = CliRunner()


def test_app_list_help():
    from onepanel.cli.application import app

    result = runner.invoke(app, ["list", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output
    assert "--page" in result.output
    assert "--page-size" in result.output


def test_app_info_help():
    from onepanel.cli.application import app

    result = runner.invoke(app, ["info", "--help"])
    assert result.exit_code == 0
    assert "key" in result.output.lower()

