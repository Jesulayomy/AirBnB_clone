#!/usr/bin/env python3
""" Amenities class that inherits from the baseModel """

from models.base_model import BaseModel


class Amenity(BaseModel):
    """ city subclass of BaseModel """

    def __init__(self, *args, **kwargs):
        """ initialization steps """

        self.name = ""
        super().__init__(*args, **kwargs)
