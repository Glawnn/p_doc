""" Entry point for the application. """

import argparse
from p_doc.config_manager import ConfigManager, Layer
from p_doc.config_manager.default_config import DefaultConfig


def init_config(parser):
    """Initialize the configuration."""
    config_manager = ConfigManager()
    config_manager.add_layer(Layer("default", DefaultConfig.as_dict(), None))
    config_manager.add_layer(Layer.load_from_args_parser(parser))
    config_manager.compute_config()
    return config_manager


def main():
    """Main function."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-path", default=None, help="Output path")

    print("Hello World!")
    print(init_config(parser).get_config())


if __name__ == "__main__":
    main()
