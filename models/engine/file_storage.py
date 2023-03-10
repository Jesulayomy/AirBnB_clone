#!/usr/bin/env python3
""" Handles file storing capabilieties """

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class FileStorage:
    """
        FileStorage class that handles serialization and
        deserialization to and from json files
    """

    __file_path = "file.json"
    __objects = {}
    md = {
            "BaseModel": BaseModel,
            "User": User,
            "Place": Place,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Review": Review
            }

    def all(self):
        """
            Returns the dictionary __objects that contains objects keyed by
            their classnames and id ("<ClassName.id>: <class '<classname>'>")
        """

        return FileStorage.__objects

    def new(self, obj):
        """
            sets in __objects the new obj
            with key <obj class name>.id
        """

        FileStorage.__objects[f"{obj.__class__.__name__}.{obj.id}"] = obj

    def save(self):
        """
            Serializes __objects to the JSON file (path: __file_path)
        """

        filename = FileStorage.__file_path
        objects_as_dicts = {}

        for key in self.__objects.keys():
            value_as_dict = self.__objects[key].to_dict()
            objects_as_dicts[key] = value_as_dict

        string = json.dumps(objects_as_dicts)

        with open(filename, "w") as fl:
            fl.write(string)

    def reload(self):
        """
            Reloads a json representation from the __file_path
        """

        filename = FileStorage.__file_path

        dicts_obj = {}
        dicts_dict = {}
        try:
            with open(filename, "r") as fl:
                string_rep = fl.read()
            dicts_dict = json.loads(string_rep)
            for key in dicts_dict.keys():
                d = dicts_dict[key]
                for md_key in self.md.keys():
                    if md_key == key[:len(md_key)]:
                        new = self.md[md_key](**d)
                dicts_obj[key] = new
            FileStorage.__objects = dicts_obj
        except FileNotFoundError:
            pass
