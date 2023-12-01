import argparse
from pathlib import Path

import pyperclip

pastes_path: Path = Path.home() / ".grab"


def copy_paste(args: argparse.Namespace) -> None:
    """copy a paste to the clipboard"""

    paste_path: Path = pastes_path / args.paste
    if not paste_path.exists():
        print(f"error: paste '{args.paste}' does not exist")
        return

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

    paste_path: Path = pastes_path / args.paste
    with Path.open(paste_path, mode="w") as f:
        f.write(args.content)

    print(f"paste '{args.paste}' saved (size: {paste_path.stat().st_size} bytes)")


def rm_paste(args: argparse.Namespace) -> None:
    """remove a paste"""

    paste_path: Path = pastes_path / args.paste
    if paste_path.exists():
        paste_path.unlink()
        print(f"paste '{args.paste}' removed")
    else:
        print(f"error: paste '{args.paste}' does not exist")


def list_pastes(_: argparse.Namespace) -> None:
    """list all available pastes"""

    if len(list(pastes_path.iterdir())) == 0:
        print("error: no pastes available")
        return

    print("available pastes:")
    for paste in pastes_path.iterdir():
        print(f" - {paste.stem} (size: {paste.stat().st_size} bytes)")


def main() -> None:
    # making sure the pastes directory exists
    if not pastes_path.exists():
        pastes_path.mkdir()

    parser = argparse.ArgumentParser(
        description="simple paste system",
        epilog="source code: https://github.com/st0rmw1ndz/grab",
        prog="grab",
    )
    subparsers = parser.add_subparsers(
        dest="command",
        title="commands",
    )

    # copy a paste to the clipboard
    copy_parser = subparsers.add_parser("copy", help="copy a paste to the clipboard")
    copy_parser.add_argument("paste", help="name of the paste")
    copy_parser.set_defaults(func=copy_paste)

    # write a new paste
    save_parser = subparsers.add_parser("write", help="write a new paste")
    save_parser.add_argument(
        "paste",
        help="name of the paste",
    )
    save_parser.add_argument(
        "content",
        help="content of the paste (string literal or file path)",
        nargs="?",
        default="",
    )
    save_parser.set_defaults(func=write_paste)

    # remove a paste
    rm_parser = subparsers.add_parser("rm", help="remove a paste")
    rm_parser.add_argument(
        "paste",
        help="name of the paste",
    )
    rm_parser.set_defaults(func=rm_paste)

    # list all available pastes
    list_parser = subparsers.add_parser("list", help="list all available pastes")
    list_parser.set_defaults(func=list_pastes)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return
    args.func(args)


if __name__ == "__main__":
    main()
