#!/usr/bin/env python3
""" user class that inherits from the baseModel """

from models.base_model import BaseModel


class City(BaseModel):
    """ city subclass of BaseModel """

    def __init__(self, *args, **kwargs):
        """ initialization steps """

        self.state_id = ""
        self.name = ""
        super().__init__(*args, **kwargs)
