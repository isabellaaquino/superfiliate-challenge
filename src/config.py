import json
from functools import lru_cache

from schemas.config.rules import CollectionDiscountConfig


def load_config(file_path: str) -> CollectionDiscountConfig:
    with open(file_path, "r") as file:
        config_data = json.load(file)
        return CollectionDiscountConfig(**config_data)


@lru_cache
def get_config():
    config = load_config("config.json")
    return config
