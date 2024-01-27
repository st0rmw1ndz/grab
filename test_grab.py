from click.testing import CliRunner

from grab.__main__ import cli

runner = CliRunner()


def test_touch_command():
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["touch", "test_paste"])
        assert result.exit_code == 0
        assert "Successfully created paste 'test_paste'." in result.output


def test_write_command():
    with runner.isolated_filesystem():
        runner.invoke(cli, ["touch", "test_paste"])
        result = runner.invoke(cli, ["write", "test_paste", "Hello, World!"])
        assert result.exit_code == 0
        assert "Successfully written to paste 'test_paste'." in result.output


def test_get_command():
    with runner.isolated_filesystem():
        runner.invoke(cli, ["touch", "test_paste"])
        runner.invoke(cli, ["write", "test_paste", "Hello, World!"])
        result = runner.invoke(cli, ["get", "test_paste"])
        assert result.exit_code == 0
        assert "Hello, World!" in result.output


def test_rm_command():
    with runner.isolated_filesystem():
        runner.invoke(cli, ["touch", "test_paste"])
        result = runner.invoke(cli, ["rm", "test_paste"])
        assert result.exit_code == 0
        assert "Successfully removed paste 'test_paste'." in result.output
