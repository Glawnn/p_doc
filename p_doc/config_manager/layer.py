""" Layer class to store the configuration of a layer. """

import argparse
import json


class Layer:
    """Layer class to store the configuration of a layer."""

    def __init__(self, name, config_json=None, path=None):
        self.name = name
        self.path = path
        if config_json is None:
            config_json = {}
        self.config_json = config_json

    @staticmethod
    def load_from_dict(name: str = "dict", config_json: dict = None, path=None):
        """Load a layer from a dictionary."""
        if config_json is None:
            config_json = {}
        return Layer(name, config_json, path)

    @staticmethod
    def load_from_json_file(name: str = "file", filename=None):
        """Load a layer from a json file."""
        config_dict = {}
        with open(filename, "r", encoding="utf-8") as file:
            config_dict = json.load(file)
        return Layer.load_from_dict(name, config_dict, filename)

    @staticmethod
    def load_from_args_parser(args_parser: argparse.Namespace):
        """Load a layer from an args parser."""
        args = vars(args_parser)
        # remove none values
        for key in list(args.keys()):
            if args[key] is None:
                del args[key]
        return Layer.load_from_dict("args_parser", args, None)

    def update_config(self, config_json):
        """Update the configuration of the layer."""
        self.config_json.update(config_json)

    def get_config(self):
        """Get the configuration of the layer."""
        return self.config_json

    def __str__(self):
        """String representation of the layer."""
        return f"Layer {self.name} with config {self.config_json}"
