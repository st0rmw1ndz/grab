import argparse
from pathlib import Path

from grab.paste_operations import ensure_paste_exists, get_paste_path


@ensure_paste_exists
def export_paste(args: argparse.Namespace) -> None:
    """export a paste"""

    paste_path: Path = get_paste_path(args.paste)
    output_path: Path = Path(args.output).expanduser()
    # create the output directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with Path.open(paste_path, mode="r") as f:
        text = f.read()

    with Path.open(args.output, mode="w") as f:
        f.write(text)

    print(f"paste '{args.paste}' exported to '{args.output}'")
