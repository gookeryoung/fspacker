import json
import logging
import typing

from fspacker.config import CONFIG_FILEPATH

_json_dict: typing.Dict[str, typing.Any] = {}

__all__ = [
    "get_json_value",
    "update_json_values",
]


def get_json_value(key: str) -> typing.Any:
    global _json_dict

    if not len(_json_dict):
        if CONFIG_FILEPATH.is_file():
            with open(CONFIG_FILEPATH) as fr:
                _json_dict = json.load(fr)
        else:
            logging.info("Both json dict and file are not valid")
            return None

    if key not in _json_dict:
        logging.warning(f"Key [{key}] not found in json dict")
        return None

    return _json_dict[key]


def update_json_values(updates: typing.Dict[str, typing.Any]):
    """Update [key, value] in json file

    Args:
        updates (typing.Dict[str, typing.Any]): update values
    """
    global _json_dict

    if not len(_json_dict):
        if CONFIG_FILEPATH.is_file():
            with open(CONFIG_FILEPATH) as fr:
                _json_dict = json.load(fr)

    for key, value in updates.items():
        _json_dict[key] = value

    with open(CONFIG_FILEPATH, "w") as fw:
        json.dump(_json_dict, fw, indent=4, ensure_ascii=False)
