from serialize import ISerialize
import Utility.logger as logger
import json
import os


@logger.trace_class
class Saver:
    def __init__(self):
        self._config_path: "str" = "./config.json"
        self._objects: "dict[str, ISerialize]" = {}
        self._dicts: "dict[str, dict]" = {}
        self.load_config()

    def register(self, object: "ISerialize"):
        if object.__class__.__name__ in self._dicts:
            dict_ = self._dicts.pop(object.__class__.__name__)
            object.deserialize(dict_)
        self._objects[object.__class__.__name__] = object

    def save_config(self):
        objects_to_dicts = {}
        for object in self._objects.values():
            objects_to_dicts[object.__class__.__name__] = object.serialize()
        with open(os.path.abspath(self._config_path), "w", encoding="utf-8") as file:
            json.dump(objects_to_dicts, file, indent=4, ensure_ascii=False)

    def load_config(self):
        if os.path.exists(os.path.abspath(self._config_path)):
            with open(os.path.abspath(self._config_path), "r", encoding="utf-8") as file:
                try:
                    self._dicts = json.load(file)
                except Exception:
                    self._dicts = {}
                    self.save_config()
