import json
import os
import pytest
from p_doc.config_manager.config_manager import ConfigManager
from p_doc.config_manager.layer import Layer

class TestConfigManager:
    def test_init_base(self):
        config_manager = ConfigManager()
        assert config_manager.layers == []
        assert config_manager.global_config == {}

    @pytest.mark.parametrize("layer", [
        pytest.param(Layer("test0", {"test": "test"}, "fake/path"), id="normal case"),
        pytest.param(Layer("test1", {}, "fake/path"), id="empty json"),
        pytest.param(Layer("test2", {"test": "test"}, None), id="empty path"),
        pytest.param(Layer("test3", {}, None), id="empty json and path"),
    ])
    def test_add_layer(self, layer):
        config_manager = ConfigManager()
        config_manager.add_layer(layer)
        assert config_manager.layers == [layer]

    @pytest.mark.parametrize("layers", [
        pytest.param([Layer("test0", {"test": "test"}, "fake/path"), Layer("test1", {}, "fake/path")], id="normal case"),
        pytest.param([Layer("test2", {"test": "test"}, None), Layer("test3", {}, None)], id="empty path"),
    ])
    def test_get_layers(self, layers):
        config_manager = ConfigManager()
        for layer in layers:
            config_manager.add_layer(layer)
        assert config_manager.get_layers() == layers

    @pytest.mark.parametrize("layers", [
        pytest.param([Layer("test0", {"test": "test"}, "fake/path"), Layer("test1", {}, "fake/path")], id="normal case"),
        pytest.param([Layer("test2", {"test": "test"}, None), Layer("test3", {}, None)], id="empty path"),
    ])
    def test_get_layer(self, layers):
        config_manager = ConfigManager()
        for layer in layers:
            config_manager.add_layer(layer)
        for layer in layers:
            assert config_manager.get_layer(layer.name) == layer

    @pytest.mark.parametrize("layers", [
        pytest.param([Layer("test0", {"test": "test"}, "fake/path"), Layer("test1", {}, "fake/path")], id="normal case"),
        pytest.param([Layer("test2", {"test": "test"}, None), Layer("test3", {}, None)], id="empty path"),
    ])
    def test_compute_config(self, layers):
        config_manager = ConfigManager()
        for layer in layers:
            config_manager.add_layer(layer)
        config_manager.compute_config()
        global_config = {}
        for layer in layers:
            global_config.update(layer.get_config())
        assert config_manager.global_config == global_config

    @pytest.mark.parametrize("layers", [
        pytest.param([Layer("test0", {"test": "test"}, "fake/path"), Layer("test1", {}, "fake/path")], id="normal case"),
        pytest.param([Layer("test2", {"test": "test"}, None), Layer("test3", {}, None)], id="empty path"),
    ])
    def test_get_config(self, layers):
        config_manager = ConfigManager()
        for layer in layers:
            config_manager.add_layer(layer)
        config_manager.compute_config()
        global_config = {}
        for layer in layers:
            global_config.update(layer.get_config())
        assert config_manager.get_config() == global_config

    @pytest.mark.parametrize("layers", [
        pytest.param([Layer("test0", {"test": "test"}, "fake/path"), Layer("test1", {}, "fake/path")], id="normal case"),
        pytest.param([Layer("test2", {"test": "test"}, None), Layer("test3", {}, None)], id="empty path"),
    ])
    def test_update_layer(self, layers):
        config_manager = ConfigManager()
        for layer in layers:
            config_manager.add_layer(layer)
        config_manager.compute_config()
        global_config = {}
        for layer in layers:
            global_config.update(layer.get_config())
        for layer in layers:
            layer.update_config({"test2": "test2"})
            config_manager.update_layer(layer.name, {"test2": "test2"})
            global_config.update({"test2": "test2"})
        assert config_manager.get_config() == global_config

    @pytest.mark.parametrize("layers", [
        pytest.param([Layer("test0", {"test": "test"}, "fakeconf.json"), Layer("test1", {}, "fakeconf2.json")], id="normal case"),
        pytest.param([Layer("test2", {"test": "test"}, None), Layer("test3", {}, None)], id="empty path"),
    ])
    def test_save_new_config_file(self, layers):
        config_manager = ConfigManager()
        for layer in layers:
            config_manager.add_layer(layer)
        config_manager.compute_config()
        global_config = {}
        for layer in layers:
            global_config.update(layer.get_config())
        config_manager.save_new_config_file()
        for layer in layers:
            if layer.path:
                with open(layer.path, "r", encoding="utf-8") as file:
                    result = json.load(file) == layer.get_config()
                if os.path.exists(layer.path):
                    os.remove(layer.path)
                assert result
