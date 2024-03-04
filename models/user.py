from pony.orm import *
from .base import db

class User(db.Entity):
    username = PrimaryKey(str)
    fullname = Required(str)
    comments = Set('Comment', reverse='author')