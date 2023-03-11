#!/usr/bin/env python3
""" user class that inherits from the baseModel """

from models.base_model import BaseModel


class User(BaseModel):
    """ User class which is a subclass of BaseModel """

    email = ""
    password = ""
    first_name = ""
    last_name = ""
