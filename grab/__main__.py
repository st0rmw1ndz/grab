import argparse

from grab import commands
from grab.utils import ensure_pastes_directory_exists


def main() -> None:
    ensure_pastes_directory_exists()

    parser = argparse.ArgumentParser(
        description="simple paste system",
        epilog="source code: https://github.com/st0rmw1ndz/grab",
        prog="grab",
    )
    subparsers = parser.add_subparsers(dest="command", title="commands")

    # copy a paste to the clipboard
    copy_parser = subparsers.add_parser("copy", help="copy a paste to the clipboard")
    copy_parser.add_argument("paste", help="name of the paste")
    copy_parser.set_defaults(func=commands.copy_paste)

    # write a new paste
    save_parser = subparsers.add_parser("write", help="write a new paste")
    save_parser.add_argument("paste", help="name of the paste")
    save_parser.add_argument(
        "content",
        help="content of the paste (string literal or file path) (default: clipboard)",
        nargs="?",
        default="",
    )
    save_parser.set_defaults(func=commands.write_paste)

    # remove a paste
    rm_parser = subparsers.add_parser("rm", help="remove a paste")
    rm_parser.add_argument("paste", help="name of the paste")
    rm_parser.set_defaults(func=commands.rm_paste)

    # list all available pastes
    list_parser = subparsers.add_parser("list", help="list all available pastes")
    list_parser.set_defaults(func=commands.list_pastes)

    # open a paste in the default text editor
    edit_parser = subparsers.add_parser(
        "edit", help="open a paste in the default text editor"
    )
    edit_parser.add_argument("paste", help="name of the paste")
    edit_parser.set_defaults(func=commands.edit_paste)

    # rename a paste
    rename_parser = subparsers.add_parser("rename", help="rename a paste")
    rename_parser.add_argument("paste", help="old name of the paste")
    rename_parser.add_argument("new", help="new name of the paste")
    rename_parser.set_defaults(func=commands.rename_paste)

    # view a paste
    view_parser = subparsers.add_parser("view", help="view a paste")
    view_parser.add_argument("paste", help="name of the paste")
    view_parser.set_defaults(func=commands.view_paste)

    # parse the arguments
    args = parser.parse_args()
    # print help if no command is given
    if not args.command:
        parser.print_help()
        return
    # call the function associated with the command
    args.func(args)


if __name__ == "__main__":
    main()
