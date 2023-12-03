import argparse
from pathlib import Path

from grab.paste_operations import ensure_paste_exists, get_paste_path


@ensure_paste_exists
def rename_paste(args: argparse.Namespace) -> None:
    """rename a paste"""

    paste_path: Path = get_paste_path(args.paste)
    new_paste_path: Path = get_paste_path(args.new)

    paste_path.rename(new_paste_path)
    print(f"paste '{args.paste}' renamed to '{args.new}'")
