from pathlib import Path

import click
import pyperclip

from grab import __version__, api
from grab.const import CONFIG_PATH
from grab.errors import PasteNotFoundError


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
@click.version_option(__version__)
@click.pass_context
def cli(ctx: click.Context) -> None:
    """A stupidly simple paste system.

    Copyright (c) 2024 frosty.
    """
    api.ensure_required_files()
    ctx.ensure_object(dict)
    try:
        config_data = api.validate_config(api.read_config(CONFIG_PATH))
        ctx.obj["config"] = config_data
    except Exception as e:
        click.echo(f"Error: Failed parsing the config file:\n{e}")
        ctx.exit(1)


@cli.group("config")
def config_group():
    """Config options."""

    pass


@config_group.command("edit")
@click.pass_context
@click.argument("editor", type=str, default="")
def edit_config(ctx: click.Context, editor: str) -> None:
    """Edit config file using a text editor.

    If an EDITOR is not supplied, it will use the one from your config file.
    """
    editor = ctx.obj["config"]["editor"] if not editor else editor
    try:
        api.edit_config(editor)
    except FileNotFoundError:
        click.echo(
            "The editor you've supplied in your config file cannot be found."
        )
        click.echo(
            "If you'd like to edit the config file manually, you can access "
            f"it at '{CONFIG_PATH}'."
        )
        ctx.exit(1)


@config_group.command("reset")
@click.pass_context
@click.option(
    "--yes",
    "-y",
    is_flag=True,
    help="Bypass confirmation and reset to defaults.",
)
def reset_config(ctx: click.Context, yes: bool):
    """Reset config file to defaults."""

    if not yes:
        confirmed = click.confirm(
            "Are you sure you want to reset to defaults?", default=True
        )
        if not confirmed:
            click.echo("Reset operation aborted.")
            return

    api.dump_default_config()
    click.echo("Config file has been reset to defaults.")


@cli.command("get")
@click.pass_context
@click.option(
    "--copy", is_flag=True, help="Copy the content to the clipboard."
)
@click.argument("paste", type=str)
@click.argument("location", type=str, default="")
def get_command(
    ctx: click.Context, copy: bool, paste: str, location: str
) -> None:
    """Get the content of a paste.

    Output is written to stdout if no LOCATION is given.
    """
    try:
        content = api.get_paste_content(paste)
        if not location:
            click.echo(content)
        else:
            location_path = Path(location).expanduser()
            if location_path.is_dir():
                click.echo(f"Error: '{location}' is a directory.")
                return
            with location_path.open(mode="w") as f:
                f.write(content)
        if copy:
            pyperclip.copy(content)
    except PasteNotFoundError:
        click.echo(f"Error: Paste '{paste}' not found.")
        ctx.exit(1)
    except PermissionError:
        click.echo(f"Error: Permission denied to write to '{location}'.")
        ctx.exit(1)
    except Exception as e:
        click.echo(
            f"Error: Something went wrong getting content of paste '{paste}':\n{e}"
        )
        ctx.exit(1)


@cli.command("write")
@click.pass_context
@click.argument("paste", type=str)
@click.argument("content", type=str, default="")
def write_command(ctx: click.Context, paste: str, content: str) -> None:
    """Write content to a paste.

    If it doesn't exist, it will be created.
    """
    try:
        if content == "":
            content = "\n".join(pyperclip.paste().splitlines())
        api.write_paste(paste, content)
        click.echo(f"Successfully written to paste '{paste}'.")
    except Exception as e:
        click.echo(
            f"Error: Something went wrong writing to paste '{paste}':\n{e}"
        )
        ctx.exit(1)


@cli.command("rename")
@click.pass_context
@click.argument("paste", type=str)
@click.argument("name", type=str)
def rename_command(ctx: click.Context, paste: str, name: str) -> None:
    """Rename a paste."""

    try:
        api.rename_paste(paste, name)
        click.echo(f"Successfully renamed paste '{paste}' to '{name}'.")
    except Exception as e:
        click.echo(
            f"Error: Something went wrong renaming paste '{paste}':\n{e}"
        )
        ctx.exit(1)


@cli.command("rm")
@click.pass_context
@click.argument("paste", type=str)
def rm_command(ctx: click.Context, paste: str) -> None:
    """Remove a paste."""

    try:
        api.rm_paste(paste)
        click.echo(f"Successfully removed paste '{paste}'.")
    except Exception as e:
        click.echo(
            f"Error: Something went wrong removing paste '{paste}':\n{e}"
        )
        ctx.exit(1)


@cli.command("touch")
@click.pass_context
@click.argument("paste", type=str)
def touch_command(ctx: click.Context, paste: str) -> None:
    """Create a paste with no content."""

    try:
        api.write_paste(paste, "")
        click.echo(f"Successfully created paste '{paste}'.")
    except Exception as e:
        click.echo(
            f"Error: Something went wrong creating paste '{paste}':\n{e}"
        )
        ctx.exit(1)


@cli.command("ls")
@click.pass_context
def ls_command(ctx: click.Context) -> None:
    """List the pastes available."""

    pastes = api.get_paste_list()
    if not pastes:
        click.echo("Error: No pastes found.")
        ctx.exit(1)

    click.echo("Pastes:")
    for name, size in pastes:
        click.echo(f" - {name} ({size} bytes)")


@cli.command("edit")
@click.pass_context
@click.argument("paste", type=str)
@click.argument("editor", type=str, default="")
def edit_command(ctx: click.Context, paste: str, editor: str) -> None:
    """Edit a paste using a text editor.

    If an EDITOR is not supplied, it will use the one from your config file.
    """
    try:
        editor = ctx.obj["config"]["editor"] if not editor else editor
        api.edit_paste(paste, editor)
    except PasteNotFoundError:
        click.echo(f"Error: Paste '{paste}' not found.")
        ctx.exit(1)
    except Exception as e:
        click.echo(
            f"Error: Something went wrong editing paste '{paste}':\n{e}"
        )
        ctx.exit(1)


if __name__ == "__main__":
    cli()
