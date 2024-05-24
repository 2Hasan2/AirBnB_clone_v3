#!/usr/bin/python3
"""
initialize the models package
"""

from os import getenv
from models.engine.file_storage import FileStorage


storage_t = getenv("HBNB_TYPE_STORAGE")

# if storage_t == "db":
# i commented this out because, there is error in the  DBStorage class 😎
#     from models.engine.db_storage import DBStorage
#     storage = DBStorage()
# else:
storage = FileStorage()
storage.reload()
