from __future__ import annotations

from typer.testing import CliRunner

runner = CliRunner()


def test_host_help():
    from onepanel.cli.host import app

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    output = result.output.lower()
    assert "list" in output
    assert "tree" in output
    assert "commands" in output
    assert "ssh-status" in output
    assert "ssh-logs" in output
    assert "tool-status" in output


def test_host_list_help():
    from onepanel.cli.host import app

    result = runner.invoke(app, ["list", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output
    assert "--page" in result.output
    assert "--page-size" in result.output


def test_host_tree_help():
    from onepanel.cli.host import app

    result = runner.invoke(app, ["tree", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output


def test_host_commands_help():
    from onepanel.cli.host import app

    result = runner.invoke(app, ["commands", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output


def test_host_ssh_status_help():
    from onepanel.cli.host import app

    result = runner.invoke(app, ["ssh-status", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output


def test_host_ssh_logs_help():
    from onepanel.cli.host import app

    result = runner.invoke(app, ["ssh-logs", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output
    assert "--status" in result.output
    assert "--page" in result.output
    assert "--page-size" in result.output


def test_host_tool_status_help():
    from onepanel.cli.host import app

    result = runner.invoke(app, ["tool-status", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output
