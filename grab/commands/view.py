import argparse
from pathlib import Path

from grab.paste_operations import ensure_paste_exists, get_paste_path


@ensure_paste_exists
def view_paste(args: argparse.Namespace) -> None:
    """view a paste"""

    paste_path: Path = get_paste_path(args.paste)

    with Path.open(paste_path, mode="r") as f:
        text = f.read()

    print(text)
