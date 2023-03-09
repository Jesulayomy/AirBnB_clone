#!/usr/bin/env python3
""" Init module for classes defined and mini usage """

from models.engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()
