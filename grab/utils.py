from functools import wraps
from pathlib import Path

from grab import pastes_folder


def ensure_pastes_directory_exists() -> None:
    """ensure the pastes directory exists"""

    if not pastes_folder.exists():
        pastes_folder.mkdir()


def ensure_paste_exists(func):
    @wraps(func)
    def wrapper(args):
        paste_path: Path = get_paste_path(args.paste)
        if not paste_path.exists():
            print(f"error: paste '{args.paste}' does not exist")
            return

        return func(args)

    return wrapper


def get_paste_path(paste_name: str) -> Path:
    """get the path of a paste"""

    return pastes_folder / (paste_name + ".txt")
