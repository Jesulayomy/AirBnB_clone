#!/usr/bin/env python3
""" state class """

from models.base_model import BaseModel


class State(BaseModel):
    """ suclass of the basemodel """

    def __init__(self, *args, **kwargs):
        """ initialization of the state class """

        self.name = ""
        super().__init__(*args, **kwargs)
