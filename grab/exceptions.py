#  Copyright (c) 2023 frosty.
#
#  This file is released under the "MIT License". Please see the LICENSE file that should have
#  been included as part of this package for more information.

from typing import List


class GrabException(Exception):
    """Base exception for all custom exceptions."""


class PasteNotFoundError(GrabException):
    def __init__(self, paste: str) -> None:
        super().__init__(f"Paste '{paste}' not found.")


class DisallowedPathDirectoryError(GrabException):
    def __init__(self) -> None:
        super().__init__("Invalid path! File exceeds the allowed directory.")


class InvalidConfigError(GrabException):
    def __init__(self, invalid_keys: List[str]) -> None:
        super().__init__(
            f"Config file contains invalid keys: {', '.join(invalid_keys)}"
        )
