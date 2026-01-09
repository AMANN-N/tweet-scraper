import os

import yaml

from src.core.exceptions import MissingConfigError
from src.models import ConfigModel, SearchConfig


def validate_env_vars() -> None:
    required = ["X_BEARER_TOKEN"]
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        raise MissingConfigError(f"Missing environment variables: {', '.join(missing)}")


def load_config(config_path: str) -> ConfigModel:
    if not os.path.exists(config_path):
        raise MissingConfigError(f"Config file not found: {config_path}")

    with open(config_path) as f:
        raw_config = yaml.safe_load(f)

    return ConfigModel(
        target_username=raw_config.get("target_username"),
        search=SearchConfig(**raw_config.get("search", {})),
        topics=raw_config.get("topics", {}),
        output_file=raw_config.get("output_file", "tweets.md"),
    )
