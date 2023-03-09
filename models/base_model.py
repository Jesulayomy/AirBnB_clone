#!/usr/bin/env python3
""" The base model class """

import json
import models
import datetime
from uuid import uuid4


class BaseModel:
    """ defines common attributes for the other classes """

    def __init__(self, *args, **kwargs):
        """ initializes the base model """

        if kwargs is not None and len(kwargs) != 0:
            for key, value in kwargs.items():
                if key[-6:] == "ted_at":
                    setattr(self, key, datetime.datetime.fromisoformat(value))
                elif key == "__class__":
                    pass
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.datetime.now()
            self.updated_at = datetime.datetime.now()
            models.storage.new(self)

    def __str__(self):
        """ prints a string representation of the basemodel object """

        return "[{}] ({}) {}".format(
            self.__class__.__name__,
            self.id,
            str(self.__dict__)
            )

    def save(self):
        """ saves with the current datetime """

        self.updated_at = datetime.datetime.now()
        models.storage.save()

    def to_dict(self):
        """
            returns a dictionary containing all
            keys/values of __dict__ of the instance
        """

        ret = {}
        for key, value in self.__dict__.items():
            if key[-6:] == 'ted_at':
                ret[key] = datetime.datetime.isoformat(value)
            else:
                ret[key] = value
        ret["__class__"] = "{}".format(self.__class__.__name__)

        return ret
