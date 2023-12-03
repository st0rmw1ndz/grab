import argparse

from grab import pastes_folder


def ls_pastes(_: argparse.Namespace) -> None:
    """list all available pastes"""

    if len(list(pastes_folder.iterdir())) == 0:
        print("error: no pastes available")
        return

    print("available pastes:")
    for paste in pastes_folder.iterdir():
        print(f" - {paste.stem} (size: {paste.stat().st_size} bytes)")
