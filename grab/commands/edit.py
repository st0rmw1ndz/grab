import argparse
import webbrowser
from pathlib import Path

from grab.paste_operations import ensure_paste_exists, get_paste_path


@ensure_paste_exists
def edit_paste(args: argparse.Namespace) -> None:
    """open a paste in the default text editor"""

    paste_path: Path = get_paste_path(args.paste)
    webbrowser.open(paste_path.as_uri())
