#!/usr/bin/env python3
""" This script defines the BaseModel class """

import json
import models
import datetime
from uuid import uuid4


class BaseModel:
    """
        BaseModel defines common attributes for the other classes.
        Super class of (Amenity, City, Place, Review, State, User)
    """

    def __init__(self, *args, **kwargs):
        """ initializes the BaseModel """

        if kwargs is not None and len(kwargs) != 0:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    setattr(self, key, datetime.datetime.fromisoformat(value))
                elif key == "__class__":
                    pass
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.datetime.now()
            self.updated_at = self.created_at
            models.storage.new(self)

    def __str__(self):
        """ Returns the string representation of the basemodel object """

        return "[{}] ({}) {}".format(
            self.__class__.__name__,
            self.id,
            str(self.__dict__)
            )

    def save(self):
        """ Saves updates to the object to the file with current datetime """

        self.updated_at = datetime.datetime.now()
        models.storage.save()

    def to_dict(self):
        """
            Returns a dictionary containing all keys/values
            of __dict__(all attributes) of the object
        """

        ret = {}
        for key, value in self.__dict__.items():
            if isinstance(value, datetime.datetime):
                ret[key] = datetime.datetime.isoformat(value)
            else:
                ret[key] = value
        ret["__class__"] = "{}".format(self.__class__.__name__)

        return ret
