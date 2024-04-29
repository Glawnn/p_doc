import json
import os
import pytest
from p_doc.config_manager.layer import Layer

class TestLayer:
    @pytest.mark.parametrize("name, config_json, path", [
        pytest.param("test0", {"test": "test"}, "fake/path", id="normal case"),
        pytest.param("test2", {}, "fake/path", id="empty json"),
        pytest.param("test3", {"test": "test"}, None, id="empty path"),
        pytest.param("test4", {}, None, id="empty json and path"),
    ])
    def test_init_base(self, name, config_json, path):
        layer = Layer(name, config_json, path)
        assert layer.name == name
        assert layer.config_json == config_json
        assert layer.path == path

    @pytest.mark.parametrize("name, config_json, path", [
        pytest.param("test0", {"test": "test"}, "fake/path", id="normal case"),
        pytest.param("test1", {}, "fake/path", id="empty json"),
        pytest.param("test2", {"test": "test"}, None, id="empty path"),
        pytest.param("test3", {}, None, id="empty json and path"),
    ])
    def test_load_from_dict(self, name, config_json, path):
        layer = Layer.load_from_dict(name, config_json, path)
        assert layer.name == name
        assert layer.config_json == config_json
        assert layer.path == path

    @pytest.mark.parametrize("name, config_json", [
        pytest.param("test0", {"test": "test"}, id="normal case"),
        pytest.param("test1", {}, id="empty json"),
        # pytest.param("test2", None, id="empty path"),
    ])
    def test_load_from_json_file(self, name, config_json):
        file_path = "tmp_test.json"
        with open(file_path, "w") as file:
            file.write(json.dumps(config_json))
        layer = Layer.load_from_json_file(name, file_path)

        if os.path.exists(file_path):
            os.remove(file_path)

        assert layer.name == name
        assert layer.config_json == config_json
        assert layer.path == file_path

    def test_load_from_json_file_error(self):
        with pytest.raises(FileNotFoundError):
            Layer.load_from_json_file("test", "fake/path")

    def test_load_from_args_parser(self):
        class ArgsParser:
            def __init__(self):
                self.test = "test"
                self.test2 = "test2"
            def parse_args(self):
                # fake function
                return self
        
        args_parser = ArgsParser()
        layer = Layer.load_from_args_parser(args_parser)
        assert layer.name == "args_parser"
        assert layer.config_json == vars(args_parser)
        assert layer.path == None

    def test_update_config(self):
        layer = Layer("test", {"test": "test"}, "fake/path")
        layer.update_config({"test2": "test2"})
        assert layer.config_json == {"test": "test", "test2": "test2"}

    def test_get_config(self):
        layer = Layer("test", {"test": "test"}, "fake/path")
        assert layer.get_config() == {"test": "test"}
    
    def test_str(self):
        layer = Layer("test", {"test": "test"}, "fake/path")
        assert str(layer) == "Layer test with config {'test': 'test'}"
