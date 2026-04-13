from __future__ import annotations

from typer.testing import CliRunner

runner = CliRunner()


def test_firewall_help():
    from onepanel.cli.firewall import app

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    output = result.output.lower()
    assert "status" in output
    assert "rules" in output


def test_firewall_status_help():
    from onepanel.cli.firewall import app

    result = runner.invoke(app, ["status", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output


def test_firewall_rules_help():
    from onepanel.cli.firewall import app

    result = runner.invoke(app, ["rules", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output
    assert "--page" in result.output
    assert "--page-size" in result.output

