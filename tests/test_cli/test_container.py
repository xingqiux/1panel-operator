from __future__ import annotations

from typer.testing import CliRunner

runner = CliRunner()


def test_container_list_help():
    from onepanel.cli.container import app

    result = runner.invoke(app, ["list", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output
    assert "--page" in result.output
    assert "--page-size" in result.output


def test_container_stats_help():
    from onepanel.cli.container import app

    result = runner.invoke(app, ["stats", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output

