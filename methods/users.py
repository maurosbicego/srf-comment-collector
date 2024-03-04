from models import User
from pony.orm import db_session, commit, core
import logging

@db_session
def assertUser(username: str, name: str) -> User:
    try:
        if username == "": # This is the case if SRF is commenting from their own account
            username = name
        user = User.get(username=username)
        if user is not None:
            return user
        else:
            user = User(username=username, fullname=name)
            logging.info(f"Added new user with username \"{username}\" and name \"{name}\"")
            try:
                commit()
            except core.TransactionIntegrityError as e:
                if 'UNIQUE constraint failed' in str(e):
                    logging.error(f"Error while creating user. Already exists. Username \"{username}\" and name \"{name}\"")

            return user
    except:
        logging.error(f"Unknown error while creating user. Username \"{username}\" and name \"{name}\"")