""" Entry point for the application. """

import argparse
import logging
from .utils import setup_logger
from p_doc.config_manager import ConfigManager, Layer
from p_doc.config_manager.default_config import DefaultConfig


class AppManager:
    """App manager class."""

    def __init__(self):
        """Initialize the AppManager."""
        setup_logger("app.log", logging.DEBUG)

        self.logger = logging.getLogger(__name__)
         

    def run(self):
        """Run the application."""
        self.logger.critical("Starting the application...")
        try:
            self._init()
            self._scrap()
            self._process()
            self._generate()
        except Exception as e:
            self.logger.error("An error occured: %s", str(e))
        finally:
            self.logger.critical("Application finished.")

    def _init(self):
        pass
        # config

    def _scrap(self):
        pass

    def _process(self):
        pass

    def _generate(self):
        pass

# def init_config(parser):
#     """Initialize the configuration."""
#     config_manager = ConfigManager()
#     config_manager.add_layer(Layer("default", DefaultConfig.as_dict(), None))
#     config_manager.add_layer(Layer.load_from_args_parser(parser))
#     config_manager.compute_config()
#     return config_manager


def main():
    appManager = AppManager()
    appManager.run()

if __name__ == "__main__":
    main()
