""" This module defines the EntityModule class. """

from .entity import EntityType, Entity


class EntityModule(Entity):
    """This class represents a module entity."""

    def __init__(self, path):
        super().__init__(path, EntityType.MODULE)
