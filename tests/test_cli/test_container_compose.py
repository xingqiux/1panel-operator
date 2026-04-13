from __future__ import annotations

from typer.testing import CliRunner

runner = CliRunner()


def test_container_compose_help():
    from onepanel.cli.container_compose import app

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    output = result.output.lower()
    assert "list" in output
    assert "template-list" in output
    assert "templates" in output


def test_container_compose_list_help():
    from onepanel.cli.container_compose import app

    result = runner.invoke(app, ["list", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output
    assert "--page" in result.output
    assert "--page-size" in result.output


def test_container_compose_template_list_help():
    from onepanel.cli.container_compose import app

    result = runner.invoke(app, ["template-list", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output
    assert "--page" in result.output
    assert "--page-size" in result.output


def test_container_compose_templates_help():
    from onepanel.cli.container_compose import app

    result = runner.invoke(app, ["templates", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output


def test_container_help_includes_compose_subcommand():
    from onepanel.cli.container import app

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "compose" in result.output.lower()

