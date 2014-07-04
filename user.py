
import pymongo

import utils
from database import db


class UserNotFound(Exception):
    
    def __str__(self):
        return 'User not found'


class UsernameExists(Exception):
    
    def __str__(self):
        return 'Username exists'


class User(object):

    def __init__(self, username):
        self.username = username
        
        user = db.users.find_one({'username': self.username})
        if user is not None:
            self.is_staff = user.is_staff
        else:
            raise UserNotFound

    @staticmethod
    def create(username, password, is_staff=False):
        assert username and password

        if not db.users.find_one({'username': username}):
            fields = {
                'username': username,
                'password': utils.get_hash(password),
                'is_staff': is_staff
            }

            db.users.insert(fields)
        else:
            raise UsernameExists

    @staticmethod
    def logon(username, password):
        pass
