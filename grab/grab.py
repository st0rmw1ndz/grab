#  Copyright (c) 2023 frosty.
#
#  This file is released under the "MIT License". Please see the LICENSE file that should have
#  been included as part of this package for more information.

from pathlib import Path
from typing import List, Tuple

import click
import pyperclip

import grab
from grab import api
from grab.exceptions import PasteNotFoundError


@click.group()
@click.option(
    "--config",
    default=grab.DEFAULT_CONFIG_PATH,
    help="Path to the configuration file.",
    type=click.Path(exists=True),
    show_default=True,
)
@click.pass_context
def cli(ctx: click.Context, config: str) -> None:
    """Stupidly simple paste system.

    Copyright (c) 2023 frosty.
    """
    ctx.ensure_object(dict)
    ctx.obj["config"] = config

    api.ensure_required_files()


@cli.command("get")
@click.option("--copy", is_flag=True, help="Copy the content to the clipboard.")
@click.argument("paste", type=str)
@click.argument("location", default="", type=str)
def get_command(copy: bool, paste: str, location: str) -> None:
    """Get the content of a paste.

    Output is written to stdout if no LOCATION is given.
    """
    try:
        content: str = api.get_paste_content(paste)
        if not location:
            print(content)
        else:
            location_path: Path = Path(location).expanduser()
            if location_path.is_dir():
                print(f"Error: '{location}' is a directory.")
                return
            with location_path.open(mode="w") as f:
                f.write(content)
        if copy:
            pyperclip.copy(content)
    except PasteNotFoundError:
        print(f"Error: Paste '{paste}' not found.")
    except PermissionError:
        print(f"Error: Permission denied to write to '{location}'.")
    except Exception as e:
        print(f"Error: Something went wrong getting content of paste '{paste}':\n{e}")


@cli.command("write")
@click.argument("paste", type=str)
@click.argument("content", type=str)
def write_command(paste: str, content: str) -> None:
    """Write content to a paste.

    If it doesn't exist, it will be created.
    """
    try:
        api.write_paste(paste, content)
        print(f"Successfully written to paste '{paste}'.")
    except Exception as e:
        print(f"Error: Something went wrong writing to paste '{paste}':\n{e}")


@cli.command("rename")
@click.argument("paste", type=str)
@click.argument("name", type=str)
def rename_command(paste: str, name: str) -> None:
    """Rename a paste."""

    try:
        api.rename_paste(paste, name)
        print(f"Successfully renamed paste '{paste}' to '{name}'.")
    except Exception as e:
        print(f"Error: Something went wrong renaming paste '{paste}':\n{e}")


@cli.command("rm")
@click.argument("paste", type=str)
def rm_command(paste: str) -> None:
    """Remove a paste."""

    try:
        api.rm_paste(paste)
        print(f"Successfully removed paste '{paste}'.")
    except Exception as e:
        print(f"Error: Something went wrong removing paste '{paste}':\n{e}")


@cli.command("ls")
def ls_command() -> None:
    """List the pastes available."""

    pastes: List[Tuple[str, int]] = api.get_paste_list()
    if not pastes:
        print("Error: No pastes found.")
        return

    print("Pastes:")
    for name, size in pastes:
        print(f" - {name} ({size} bytes)")


@cli.command("edit")
@click.argument("paste", type=str)
@click.argument("editor", default="", type=str)
@click.pass_context
def edit_command(ctx: click.Context, paste: str, editor: str) -> None:
    """Edit a paste using a text editor.

    If an EDITOR is not supplied, it will use the one from your config file.
    """
    try:
        # TODO: Make a wrapper so I don't have to repeat this? Wtf?
        editor = (
            api.validate_config(api.read_config(Path(ctx.obj["config"])))["editor"]
            if not editor
            else editor
        )
        api.edit_paste(paste, editor)
    except PasteNotFoundError:
        print(f"Error: Paste '{paste}' not found.")
    except Exception as e:
        print(f"Error: Something went wrong editing paste '{paste}':\n{e}")
