from __future__ import annotations

from typer.testing import CliRunner

runner = CliRunner()


def test_container_docker_help():
    from onepanel.cli.container_docker import app

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    output = result.output.lower()
    assert "status" in output
    assert "config" in output


def test_container_docker_status_help():
    from onepanel.cli.container_docker import app

    result = runner.invoke(app, ["status", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output


def test_container_docker_config_help():
    from onepanel.cli.container_docker import app

    result = runner.invoke(app, ["config", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output


def test_container_help_includes_docker_subcommand():
    from onepanel.cli.container import app

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "docker" in result.output.lower()
