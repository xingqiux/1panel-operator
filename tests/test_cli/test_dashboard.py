from __future__ import annotations

from typer.testing import CliRunner

runner = CliRunner()


def test_dashboard_help():
    from onepanel.cli.dashboard import app

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "metrics" in result.output.lower()
    assert "monitor" in result.output.lower()


def test_dashboard_os_help():
    from onepanel.cli.dashboard import app

    result = runner.invoke(app, ["os", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output


def test_dashboard_metrics_help():
    from onepanel.cli.dashboard import app

    result = runner.invoke(app, ["metrics", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output
    assert "--io" in result.output
    assert "--net" in result.output


def test_dashboard_monitor_help():
    from onepanel.cli.dashboard import app

    result = runner.invoke(app, ["monitor", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output
    assert "--start-time" in result.output
    assert "--end-time" in result.output
