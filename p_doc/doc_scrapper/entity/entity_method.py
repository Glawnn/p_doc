""" This module contains the EntityMethod class. """

from p_doc.doc_scrapper.entity.entity import Entity
from p_doc.doc_scrapper.entity.entity_type import EntityType


class EntityMethod(Entity):
    """This class represents a method entity."""

    def __init__(self, path):
        super().__init__(path, EntityType.METHOD)
        self.args = []

    def to_dict(self, recursive=True):
        return Entity.to_dict(self, recursive) | {"args": self.args}
