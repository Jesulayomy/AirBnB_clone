#!/usr/bin/python3
""" Handles file storing capabilieties """

import json
from models.base_model import BaseModel


class FileStorage:
    """ filestorage class """

    __file_path = "file.json"
    __objects = {}
    """ __objects = {'Bm.69': <object basemodel> } """

    def all(self):
        """ returns the dictionary __objects """

        return FileStorage.__objects

    def new(self, obj):
        """ sets in __objects the obj with key <obj class name>.id """

        FileStorage.__objects[f"{obj.__class__.__name__}.{obj.id}"] = obj

    def save(self):
        """ serializes __objects to the JSON file (path: __file_path) """

        filename = FileStorage.__file_path
        objects_as_dicts = {}

        for key in self.__objects.keys():
            value_as_dict = self.__objects[key].to_dict()
            objects_as_dicts[key] = value_as_dict

        string = json.dumps(objects_as_dicts)

        with open(filename, "w") as fl:
            fl.write(string)

    def reload(self):
        """ reloads a json representation """

        filename = FileStorage.__file_path

        dicts_obj = {}
        dicts_dict = {}
        try:
            with open(filename, "r") as fl:
                string_rep = fl.read()
            dicts_dict = json.loads(string_rep)
            for key in dicts_dict.keys():
                d = dicts_dict[key]
                new = BaseModel(**d)
                dicts_obj[key] = new
            FileStorage.__objects = dicts_obj
        except FileNotFoundError:
            pass
