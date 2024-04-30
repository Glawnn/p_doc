""" Module to scrap all docstrings and code structure from all files in a project path. """

import ast
import logging
import os

from p_doc.doc_scrapper.entity.entity_class import EntityClass
from p_doc.doc_scrapper.entity.entity_method import EntityMethod
from p_doc.doc_scrapper.entity.entity_module import EntityModule
from p_doc.doc_scrapper.entity.entity_folder import EntityFolder


class DocScrapper:
    """Class to scrap all docstrings and code structure from all files in a project path."""

    def __init__(self, path, ignore_dirs=None):
        self.base_path = os.path.normpath(path)
        self.logger = logging.getLogger(__name__)
        self.main_entity = None
        self.entitys = []
        self.ignore_dirs = ignore_dirs or []

    def execute(self):
        """start the scrapping process"""
        self.logger.debug("Starting scrapping process...")
        self._scrap_main_entity()
        self._scrap_dir(self.main_entity)

    def reset(self):
        """Reset the scrapping process"""
        self.logger.debug("Resetting scrapping process...")
        self.main_entity = None
        self.entitys = []

    def _scrap_main_entity(self):
        self.logger.debug("Scraping main entity")
        if not os.path.exists(self.base_path):
            raise FileNotFoundError(f"Path {self.base_path} not found")

        self.main_entity = EntityFolder(self.base_path)
        self.entitys.append(self.main_entity)

    def _scrap_dir(self, entity):
        self.logger.debug("Scraping directory %s", entity.path)
        for elem in os.listdir(entity.path):
            elem_path = os.path.join(entity.path, elem)

            if os.path.isdir(elem_path) and elem not in self.ignore_dirs:
                new_entity = EntityFolder(elem_path)
                entity.add_child(new_entity)
                self.entitys.append(new_entity)
                self._scrap_dir(new_entity)

            elif os.path.isfile(elem_path) and elem.endswith(".py"):
                self._scrap_file(elem_path, entity)

    def _scrap_file(self, path, entity):
        self.logger.debug("Scraping file %s", path)
        with open(path, "r", encoding="utf-8") as file:
            tree = ast.parse(file.read())
            new_entity = EntityModule(path)
            new_entity.docstring = ast.get_docstring(tree)
            entity.add_child(new_entity)
            self.entitys.append(new_entity)

            self._scrap_tree(tree, new_entity)

    def _scrap_tree(self, tree, entity):
        for elem in tree.body:
            if isinstance(elem, ast.FunctionDef):
                self._scrap_function(elem, entity)
            elif isinstance(elem, ast.ClassDef):
                self._scrap_class(elem, entity)

    def _scrap_function(self, func, entity):
        path = entity.path.split(".")[0]
        path = os.path.join(path, func.name)
        new_entity = EntityMethod(path)
        new_entity.docstring = ast.get_docstring(func)

        args = func.args.args
        for arg in args:
            try:
                annotation_id = arg.annotation.id
            except AttributeError:
                annotation_id = None

            arg_dict = {"name": arg.arg, "annotation": annotation_id}
            new_entity.args.append(arg_dict)

        entity.add_child(new_entity)
        self.entitys.append(new_entity)

    def _scrap_class(self, class_, entity):
        path = entity.path.split(".")[0]
        path = os.path.join(path, class_.name)
        new_entity = EntityClass(path)
        new_entity.docstring = ast.get_docstring(class_)
        entity.add_child(new_entity)
        self.entitys.append(new_entity)
        for elem in class_.body:
            if isinstance(elem, ast.FunctionDef):
                self._scrap_function(elem, new_entity)
            elif isinstance(elem, ast.ClassDef):
                self._scrap_class(elem, new_entity)
