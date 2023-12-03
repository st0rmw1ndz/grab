__all__ = ["pastes_folder"]

from pathlib import Path

pastes_folder: Path = Path.home() / ".grab"
