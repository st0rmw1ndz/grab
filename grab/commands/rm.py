import argparse
from pathlib import Path

from grab.paste_operations import ensure_paste_exists, get_paste_path


@ensure_paste_exists
def rm_paste(args: argparse.Namespace) -> None:
    """remove a paste"""

    paste_path: Path = get_paste_path(args.paste)
    paste_path.unlink()
    print(f"paste '{args.paste}' removed")
