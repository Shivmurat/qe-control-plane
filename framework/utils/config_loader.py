import os
from pathlib import Path

import yaml

class ConfigLoader:
    """
    Centralised configuration loader.

    Responsibilities:
     - Load environment-specific YAML configs
     - Provide singleton-style config access
     - Prevent repeated file reads
    """

    _config = None

    @classmethod
    def load_config(cls, environment: str = None) -> dict:
        """
        Load configuration for given environment.

        Priority:
        1. Explicit environment argument
        2. ENV environment variable
        3. Default -> Dev
        """

        if cls._config is not None:
            return cls._config

        env = (environment or os.getenv("ENV") or "dev")

        project_root = Path(__file__).resolve().parents[2]

        config_path = ( project_root / "framework" / "configs" / f"{env}.yaml")

        if not config_path.exists():
            raise FileNotFoundError(
                f"configuration file not found: {config_path}"
            )

        with open(config_path, "r") as config_file:
            cls._config = yaml.safe_load(config_file)

        return cls._config


    @classmethod
    def get(cls, key: str, default:None):
        """
        get config value by Key.
        """

        if cls._config is None:
            cls.load_config()

        return cls._config.get(key, default)

    @classmethod
    def reload(cls):
        """
        Force reload configuration.
        useful for testing
        """

        cls._config = None

