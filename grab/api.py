# TODO: Redo most of the API functions docstrings, including the parameters.

import pathlib
import subprocess
from typing import Dict, List, Tuple

import yaml

from grab.const import CONFIG_PATH, DEFAULT_CONFIG, PASTES_DIRECTORY
from grab.errors import (
    DisallowedPathDirectoryError,
    InvalidConfigError,
    PasteNotFoundError,
)


def read_config(config_file: pathlib.Path) -> Dict[str, str]:
    """Reads a file path as a YAML for use as a config.

    :return: Config data as a dictionary.
    """
    return yaml.safe_load(config_file.open())


def validate_config(config: Dict[str, str]) -> Dict[str, str]:
    """Validates a passed ditionary as a config. Any keys that aren't present
    in the default will be added with default values. Any keys that aren't
    present in the default will throw an error.

    :param config: Config dictionary.
    :return: Config with all keys required.
    """
    config = {
        key: config.get(key, DEFAULT_CONFIG[key]) for key in DEFAULT_CONFIG
    }
    if invalid_keys := [
        key for key in config.keys() if key not in DEFAULT_CONFIG
    ]:
        raise InvalidConfigError(invalid_keys=invalid_keys)
    return config


def dump_default_config() -> None:
    with CONFIG_PATH.open(mode="w") as f:
        yaml.dump(DEFAULT_CONFIG, f, default_flow_style=False)


def ensure_required_files() -> None:
    """Ensures the pastes directory and config files exist.
    They will be created if they don't exist already.

    :return: None.
    """
    if not PASTES_DIRECTORY.is_dir():
        PASTES_DIRECTORY.mkdir()
    if not CONFIG_PATH.is_file():
        CONFIG_PATH.touch()
    if not CONFIG_PATH.stat().st_size:
        dump_default_config()


def is_within_allowed_directory(path: pathlib.Path) -> bool:
    """Checks if a path is within the allowed directory of pastes.

    :param path: Path to check.
    :return: Whether it's in the allowed directory.
    """
    allowed = PASTES_DIRECTORY.resolve()
    return path.resolve().parts[: len(allowed.parts)] == allowed.parts


def does_paste_exist(paste: str) -> bool:
    """Checks whether a paste exists.

    :param paste: Paste name.
    :return: Whether it exists.
    """
    return PASTES_DIRECTORY.joinpath(paste).exists()


def write_paste(paste: str, content: str, not_found_ok=True) -> None:
    """Writes content to a paste. If it doesn't exist already and
    `not_found_ok` is True, it will be created.

    :param paste: Paste name.
    :param content: Content of the paste.
    :return: None.
    """
    if not does_paste_exist(paste) and not not_found_ok:
        raise PasteNotFoundError(paste=paste)
    with PASTES_DIRECTORY.joinpath(paste).open(mode="w") as f:
        f.write(content)


def rm_paste(paste: str) -> None:
    """Removes a paste.

    :param paste: Paste name.
    :return: None.
    """
    if not does_paste_exist(paste):
        raise PasteNotFoundError(paste=paste)
    PASTES_DIRECTORY.joinpath(paste).unlink()


def rename_paste(paste: str, name: str) -> None:
    """Renames a paste.

    :param paste: Paste name.
    :param name: New name.
    :return: None.
    """
    if not does_paste_exist(paste):
        raise PasteNotFoundError(paste=paste)
    paste_path = PASTES_DIRECTORY.joinpath(paste)
    if is_within_allowed_directory(PASTES_DIRECTORY.joinpath(name)):
        paste_path.rename(PASTES_DIRECTORY.joinpath(name))
    else:
        raise DisallowedPathDirectoryError


def get_paste_content(paste: str) -> str:
    """Gets content of a paste.

    :param paste: Paste name.
    :return: Paste content.
    """
    if not does_paste_exist(paste):
        raise PasteNotFoundError(paste=paste)
    paste_path = PASTES_DIRECTORY.joinpath(paste)
    with paste_path.open(mode="r") as f:
        return f.read()


def get_paste_list() -> List[Tuple[str, int]]:
    """Gets the pastes list. Each item in the list is a
    tuple containing the name and byte size of the paste.

    :return: List of pastes in the format of (name, byte size).
    """
    if not (pastes := [paste for paste in PASTES_DIRECTORY.iterdir()]):
        return []
    return [(paste.name, paste.stat().st_size) for paste in pastes]


def edit_paste(paste: str, editor: str) -> None:
    """Edits a paste using a specified editor. It will open in a subprocess.
    If you want specific arguments for the editor, pass them in the `editor`.

    :param paste: Paste name.
    :param editor: Command to run to edit.
    :return: None.
    """
    if not does_paste_exist(paste):
        raise PasteNotFoundError(paste=paste)
    print(editor, PASTES_DIRECTORY.joinpath(paste))
    subprocess.run([editor, PASTES_DIRECTORY.joinpath(paste)], shell=False)


def edit_config(editor: str) -> None:
    subprocess.run([editor, CONFIG_PATH], shell=True)
