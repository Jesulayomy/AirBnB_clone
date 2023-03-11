#!/usr/bin/env python3
""" user class that inherits from the baseModel """

from models.base_model import BaseModel


class City(BaseModel):
    """ city subclass of BaseModel """

    state_id = ""
    name = ""
