""" Default config """

from enum import Enum


class DefaultConfig(Enum):
    """Default configuration"""

    OUTPUT_PATH = "docs/"
    OUTPUT_FILENAME = "output"
    OUTPUT_FORMAT = "md"
    IGNORE_FILES = []
    IGNORE_FOLDER = ["__pycache__"]
    INPUT_PATH = "."

    @staticmethod
    def as_dict():
        """Convert the default config to a dictionary."""
        return {config.name.lower(): config.value for config in DefaultConfig}
