__all__ = [
    "copy_paste",
    "write_paste",
    "rm_paste",
    "list_pastes",
    "edit_paste",
    "rename_paste",
    "view_paste",
]

import argparse
import webbrowser
from pathlib import Path

import pyperclip

from grab import pastes_folder
from grab.utils import ensure_paste_exists, get_paste_path


@ensure_paste_exists
def copy_paste(args: argparse.Namespace) -> None:
    """copy a paste to the clipboard"""

    paste_path: Path = get_paste_path(args.paste)

    with Path.open(paste_path, mode="r") as f:
        text = f.read()

    pyperclip.copy(text)
    print(f"paste '{args.paste}' copied to the clipboard")


def write_paste(args: argparse.Namespace) -> None:
    """write a new paste"""

    if args.content == "":
        args.content = "\n".join(pyperclip.paste().splitlines())

    # checking if the content is a file path that exists,
    # if so, read the file and use its content
    if Path(args.content).exists():
        with Path.open(args.content, mode="r") as f:
            args.content = f.read()

    paste_path: Path = get_paste_path(args.paste)
    with Path.open(paste_path, mode="w") as f:
        f.write(args.content)

    print(f"paste '{args.paste}' saved (size: {paste_path.stat().st_size} bytes)")


@ensure_paste_exists
def rm_paste(args: argparse.Namespace) -> None:
    """remove a paste"""

    paste_path: Path = get_paste_path(args.paste)
    paste_path.unlink()
    print(f"paste '{args.paste}' removed")


def list_pastes(_: argparse.Namespace) -> None:
    """list all available pastes"""

    if len(list(pastes_folder.iterdir())) == 0:
        print("error: no pastes available")
        return

    print("available pastes:")
    for paste in pastes_folder.iterdir():
        print(f" - {paste.stem} (size: {paste.stat().st_size} bytes)")


@ensure_paste_exists
def edit_paste(args: argparse.Namespace) -> None:
    """open a paste in the default text editor"""

    paste_path: Path = get_paste_path(args.paste)
    webbrowser.open(paste_path.as_uri())


@ensure_paste_exists
def rename_paste(args: argparse.Namespace) -> None:
    """rename a paste"""

    paste_path: Path = get_paste_path(args.paste)
    new_paste_path: Path = get_paste_path(args.new)

    paste_path.rename(new_paste_path)
    print(f"paste '{args.paste}' renamed to '{args.new}'")


@ensure_paste_exists
def view_paste(args: argparse.Namespace) -> None:
    """view a paste"""

    paste_path: Path = get_paste_path(args.paste)

    with Path.open(paste_path, mode="r") as f:
        text = f.read()

    print(text)
