""" This module contains the EntityClass class. """

from p_doc.doc_scrapper.entity.entity import Entity
from p_doc.doc_scrapper.entity.entity_type import EntityType


class EntityClass(Entity):
    """This class represents a class entity."""

    def __init__(self, path):
        super().__init__(path, EntityType.CLASS)
