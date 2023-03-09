#!/usr/bin/env python3
""" reviews and ratings """

from models.base_model import BaseModel


class Review(BaseModel):
    """ reviews for basemodels """

    def __init__(self, *args, **kwargs):
        """ initialization for reviews """

        self.place_id = ""
        self.user_id = ""
        self.text = ""
        super().__init__(*args, **kwargs)
