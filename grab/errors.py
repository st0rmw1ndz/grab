from typing import List


class GrabError(Exception):
    pass


class PasteNotFoundError(GrabError):
    def __init__(self, paste: str) -> None:
        super().__init__(f"Paste '{paste}' not found.")


class DisallowedPathDirectoryError(GrabError):
    def __init__(self) -> None:
        super().__init__("Invalid path. File exceeds the allowed directory.")


class InvalidConfigError(GrabError):
    def __init__(self, invalid_keys: List[str]) -> None:
        super().__init__(
            f"Config file contains invalid keys: {', '.join(invalid_keys)}",
        )
