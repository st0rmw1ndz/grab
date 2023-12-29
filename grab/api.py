#  Copyright (c) 2023 frosty.
#
#  This file is released under the "MIT License". Please see the LICENSE file that should have
#  been included as part of this package for more information.

import subprocess
from pathlib import Path
from typing import Dict, Tuple

import yaml

from grab import DEFAULT_CONFIG, DEFAULT_CONFIG_PATH, DEFAULT_PASTES_PATH
from grab.exceptions import *


def read_config(config_file: Path) -> Dict[str, str]:
    """Reads a file path as a YAML for use as a config.
    :return: Config data as a dictionary.
    """
    return yaml.safe_load(config_file.open())


def validate_config(config: Dict[str, str]) -> Dict[str, str]:
    """Validates a passed ditionary as a config. Any keys that aren't present in the default will be
    added with default values. Any keys that aren't present in the default will throw an error.
    :param config: Config dictionary.
    :return: Config with all keys required.
    """
    config = {key: config.get(key, DEFAULT_CONFIG[key]) for key in DEFAULT_CONFIG}

    invalid_keys = [key for key in config.keys() if key not in DEFAULT_CONFIG]
    if invalid_keys:
        raise InvalidConfigError(invalid_keys=invalid_keys)

    return config


def ensure_required_files() -> None:
    """Ensures the pastes directory and config files exist.
    They will be created if they don't exist already.
    :return: None.
    """
    if not DEFAULT_PASTES_PATH.exists():
        DEFAULT_PASTES_PATH.mkdir()
    if not DEFAULT_CONFIG_PATH.exists():
        DEFAULT_CONFIG_PATH.touch()
    if not DEFAULT_CONFIG_PATH.stat().st_size:
        with DEFAULT_CONFIG_PATH.open(mode="w") as f:
            yaml.dump(DEFAULT_CONFIG, f, default_flow_style=False)


def is_within_allowed_directory(path: Path) -> bool:
    """Checks if a path is within the allowed directory of pastes.
    :param path: Path to check.
    :return: Whether it's in the allowed directory.
    """
    allowed: Path = DEFAULT_PASTES_PATH.resolve()
    return path.resolve().parts[: len(allowed.parts)] == allowed.parts


def does_paste_exist(paste: str) -> bool:
    """Checks whether a paste exists.
    :param paste: Paste name.
    :return: Whether it exists.
    """
    return DEFAULT_PASTES_PATH.joinpath(paste).exists()


def write_paste(paste: str, content: str) -> None:
    """Writes content to a paste. If it doesn't exist already, it will be created.
    :param paste: Paste name.
    :param content: Content of the paste.
    :return: None.
    """
    with DEFAULT_PASTES_PATH.joinpath(paste).open(mode="w") as f:
        f.write(content)


def rm_paste(paste: str) -> None:
    """Removes a paste.
    :param paste: Paste name.
    :return: None.
    """
    if not does_paste_exist(paste):
        raise PasteNotFoundError(paste=paste)
    DEFAULT_PASTES_PATH.joinpath(paste).unlink()


def rename_paste(paste: str, name: str) -> None:
    """Renames a paste.
    :param paste: Paste name.
    :param name: New name.
    :return: None.
    """
    if not does_paste_exist(paste):
        raise PasteNotFoundError(paste=paste)
    paste_path: Path = DEFAULT_PASTES_PATH.joinpath(paste)
    if is_within_allowed_directory(DEFAULT_PASTES_PATH.joinpath(name)):
        paste_path.rename(DEFAULT_PASTES_PATH.joinpath(name))
    else:
        raise DisallowedPathDirectoryError


def get_paste_content(paste: str) -> str:
    """Gets content of a paste.
    :param paste: Paste name.
    :return: Paste content.
    """
    if not does_paste_exist(paste):
        raise PasteNotFoundError(paste=paste)
    paste_path: Path = DEFAULT_PASTES_PATH.joinpath(paste)
    with paste_path.open(mode="r") as f:
        return f.read()


def get_paste_list() -> List[Tuple[str, int]]:
    """Gets the pastes list. Each item in the list is a
    tuple containing the name and byte size of the paste.
    :return: List of pastes in the format of (name, byte size).
    """
    if not (pastes := [paste for paste in DEFAULT_PASTES_PATH.iterdir()]):
        return []
    return [(paste.name, paste.stat().st_size) for paste in pastes]


def edit_paste(paste: str, editor: str) -> None:
    """Edits a paste using a specified editor. It will open in a subprocess. If you want
    specific arguments for the editor, pass them in the `editor`.
    :param paste: Paste name.
    :param editor: Command to run to edit.
    :return: None.
    """
    if not does_paste_exist(paste):
        raise PasteNotFoundError(paste=paste)
    subprocess.run([editor, DEFAULT_PASTES_PATH.joinpath(paste)], shell=True)