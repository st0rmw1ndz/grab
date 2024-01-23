import os
from pathlib import Path

PASTES_DIRECTORY = Path.expanduser(Path("~/.grab"))
CONFIG_PATH = Path.expanduser(Path("~/.grab.yml"))
DEFAULT_CONFIG = {
    "editor": "notepad" if os.name == "nt" else "nano",
}
