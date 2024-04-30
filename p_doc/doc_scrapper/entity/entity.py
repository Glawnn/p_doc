""" Entity class definition. """

import os
from p_doc.doc_scrapper.entity.entity_type import EntityType


class Entity:
    """This class represents an base entity."""

    def __init__(self, path, _type=EntityType.UNKNOWN):
        self.type = _type
        self.path = os.path.normpath(path)
        self.key = self._compute_key()
        self.children = {}
        self.docstring = None

    def _compute_key(self):
        """Compute the key of the entity."""
        return ".".join(self.path.split(os.sep)).replace(".py", "")

    def add_child(self, child):
        """Add a child to the entity."""
        self.children[child.key] = child

    def to_dict(self, recursive=False):
        """Return the entity as a dictionary."""
        return {
            "type": self.type.value,
            "path": self.path,
            "key": self.key,
            "children": (
                {k: v.to_dict() for k, v in self.children.items()}
                if recursive
                else list(self.children.keys())
            ),
            "docstring": self.docstring,
        }

    def tree(self):
        """Print the tree of the entity with keys"""
        return self._tree(self, 0)

    def _tree(self, entity, level):
        result = "|   " * level + "|-- " if level > 0 else "."
        result += f"{entity.key} ({entity.type.value})"
        for elem in entity.children.values():
            result += "\n" + self._tree(elem, level + 1)
        return result

    def __repr__(self):
        return f"{self.type} {self.key}"

    def __str__(self):
        return self.__repr__()
