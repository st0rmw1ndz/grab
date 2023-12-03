import argparse
from pathlib import Path

from grab.paste_operations import ensure_paste_exists, get_paste_path
from grab.uploader.catbox import CatboxUploader


@ensure_paste_exists
def upload_paste(args: argparse.Namespace) -> None:
    """upload a paste"""

    paste_path: Path = get_paste_path(args.paste)
    uploader = CatboxUploader()
    url = uploader.upload(paste_path)
    print(url)
