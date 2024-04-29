""" Entry point for the application. """

import argparse
import logging
import os

from p_doc.config_manager import ConfigManager, Layer
from p_doc.config_manager.default_config import DefaultConfig
from .utils import setup_logger


class AppManager:
    """App manager class."""

    def __init__(self):
        """Initialize the AppManager."""
        setup_logger("app.log", logging.DEBUG)
        self.logger = logging.getLogger(__name__)

        self.parser = argparse.ArgumentParser(description="Process some integers.")
        for elem in DefaultConfig.as_dict():
            elem = elem.replace("_", "-")
            self.parser.add_argument(f"--{elem}", type=str, help=f"Set the value of {elem}")
        self.args = self.parser.parse_args()

        self.config_manager = ConfigManager()

    def run(self):
        """Run the application."""
        self.logger.critical("Starting the application...")
        try:
            self._init()
            self._scrap()
            self._process()
            self._generate()
        except Exception as e:  # pylint: disable=broad-except
            self.logger.exception(e)
        finally:
            self.logger.critical("Application finished.")

    def _init(self):
        self.logger.debug("Initializing the application...")
        self.config_manager.add_layer(Layer("default", DefaultConfig.as_dict(), None))
        if os.path.exists("pdoconf.json"):
            self.logger.debug("Loading configuration from file pdoconf.json")
            self.config_manager.add_layer(Layer.load_from_json_file("config_file", "pdoconf.json"))
        else:
            self.logger.debug("No configuration file found.")
        self.config_manager.add_layer(Layer.load_from_args_parser(self.args))
        self.config_manager.compute_config()
        self.logger.debug("Configuration: %s", self.config_manager.get_config())

    def _scrap(self):
        return

    def _process(self):
        return

    def _generate(self):
        return

    def generate_config_file(self):
        """Generate a configuration file."""
        return


def main():
    """ Main function. """
    app_manager = AppManager()
    app_manager.run()


if __name__ == "__main__":
    main()
