from datetime import datetime
from pony.orm import *
from .base import db

class Comment(db.Entity):
    author = Required("User", cascade_delete=False, reverse='comments')
    article = Required("Article", cascade_delete=False, reverse='comments')
    id = PrimaryKey(int)
    text = Required(str)
    creationdate = Required(datetime)
    likes = Required(int)
    replies = Set('Comment', reverse='parentcomment')
    parentcomment = Optional("Comment", cascade_delete=False, reverse='replies')