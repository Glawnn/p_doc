""" Enum class for entity types """

from enum import Enum


class EntityType(Enum):
    """Enum class for entity types"""

    UNKNOWN = "UNKNOWN"
    MODULE = "MODULE"
    CLASS = "CLASS"
    METHOD = "METHOD"
    FOLDER = "FOLDER"
