#!/usr/bin/env python3
""" user class that inherits from the baseModel """

from models.base_model import BaseModel


class User(BaseModel):
    """ User class which is a subclass of BaseModel """

    def __init__(self, *args, **kwargs):
        """ initialization step """

        self.email = ""
        self.password = ""
        self.first_name = ""
        self.last_name = ""
        super().__init__(*args, **kwargs)
