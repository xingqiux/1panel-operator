from __future__ import annotations

from typer.testing import CliRunner

runner = CliRunner()


def test_container_image_help():
    from onepanel.cli.container_image import app

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    output = result.output.lower()
    assert "list" in output
    assert "all" in output
    assert "repo-list" in output


def test_container_image_list_help():
    from onepanel.cli.container_image import app

    result = runner.invoke(app, ["list", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output
    assert "--page" in result.output
    assert "--page-size" in result.output


def test_container_image_all_help():
    from onepanel.cli.container_image import app

    result = runner.invoke(app, ["all", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output


def test_container_image_repo_list_help():
    from onepanel.cli.container_image import app

    result = runner.invoke(app, ["repo-list", "--help"])
    assert result.exit_code == 0
    assert "--raw" in result.output
    assert "--page" in result.output
    assert "--page-size" in result.output


def test_container_help_includes_image_subcommand():
    from onepanel.cli.container import app

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "image" in result.output.lower()
