from datetime import datetime
from pony.orm import *
from .base import db


class Article(db.Entity):
    id = PrimaryKey(int)
    commentsfetched = Required(bool)
    hascomments = Required(bool)
    comments = Set('Comment', reverse='article')
    created = Optional(datetime)
    publicationdate = Optional(datetime)
    kicker = Optional(str)
    title = Optional(str)
    welcomemessage = Optional(str)
    frontendurl = Optional(str)
