""" This module is responsible for managing the configuration of the layers.
It is responsible for loading the configuration files,
updating the configuration of the layers and saving the new configuration files. """

import json
from .layer import Layer


class ConfigManager:
    """ConfigManager class to manage the configuration of the layers."""

    def __init__(self):
        self.layers = []
        self.global_config = {}

    def add_layer(self, layer: Layer):
        """Add a layer to the config manager."""
        self.layers.append(layer)

    def get_layers(self):
        """Get the list of layers."""
        return self.layers

    def get_layer(self, name):
        """Get a layer by its name."""
        for layer in self.layers:
            if layer.name == name:
                return layer
        return None

    def compute_config(self):
        """Compute the global configuration of the layers."""
        global_config = {}
        for layer in self.layers:
            global_config.update(layer.get_config())
        self.global_config = global_config

    def get_config(self):
        """Get the global configuration."""
        return self.global_config

    def update_layer(self, name, config_json, save=False):
        """Update the configuration of a layer."""
        layer = self.get_layer(name)
        if layer:
            layer.update_config(config_json)
            self.compute_config()
            if save:
                self.save_new_config_file()
            return True
        return False

    def save_new_config_file(self):
        """Save the new configuration files."""
        for layer in self.layers:
            if layer.path:
                with open(layer.path, "w", encoding="utf-8") as file:
                    json.dump(layer.get_config(), file, indent=4)
