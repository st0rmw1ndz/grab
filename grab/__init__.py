#  Copyright (c) 2023 frosty.
#
#  This file is released under the "MIT License". Please see the LICENSE file that should have
#  been included as part of this package for more information.

import os
from pathlib import Path
from typing import Dict

__all__ = ["DEFAULT_CONFIG", "DEFAULT_CONFIG_PATH", "DEFAULT_PASTES_PATH"]

DEFAULT_PASTES_PATH: Path = Path.expanduser(Path("~/.grab"))
DEFAULT_CONFIG_PATH: Path = Path.expanduser(Path("~/.grab.yml"))
DEFAULT_CONFIG: Dict[str, str] = {
    "editor": "notepad" if os.name == "nt" else "nano",
    "pastes": "~/.grab",
}
