import argparse
from pathlib import Path

import pyperclip

from grab.paste_operations import ensure_paste_exists, get_paste_path


@ensure_paste_exists
def copy_paste(args: argparse.Namespace) -> None:
    """copy a paste to the clipboard"""

    paste_path: Path = get_paste_path(args.paste)

    with Path.open(paste_path, mode="r") as f:
        text = f.read()

    pyperclip.copy(text)
    print(f"paste '{args.paste}' copied to the clipboard")
