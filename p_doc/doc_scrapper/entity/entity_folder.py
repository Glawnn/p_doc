""" This module contains the EntityFolder class. """

from .entity import EntityType, Entity


class EntityFolder(Entity):
    """This class represents a folder entity."""

    def __init__(self, path):
        super().__init__(path, EntityType.FOLDER)
