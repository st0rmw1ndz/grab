import argparse
from pathlib import Path

import pyperclip

from grab.paste_operations import get_paste_path


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
