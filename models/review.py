#!/usr/bin/env python3
""" reviews and ratings """

from models.base_model import BaseModel


class Review(BaseModel):
    """ reviews for basemodels """

    place_id = ""
    user_id = ""
    text = ""
