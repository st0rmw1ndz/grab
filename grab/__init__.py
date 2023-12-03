__all__ = ["pastes_folder"]
__version__: str = "1.0.5"

from pathlib import Path

pastes_folder: Path = Path.home() / ".grab"
