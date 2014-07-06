# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# User

import pymongo

import utils
from engine.database import db


class UserNotFound(Exception):
    
    def __str__(self):
        return 'User not found'


class UsernameExists(Exception):
    
    def __str__(self):
        return 'Username exists'


class User(object):

    def __init__(self, username):
        user = db.users.find_one({'username': username})
        
        if user is not None:
            self.username = username
            self.is_staff = user['is_staff']
        else:
            raise UserNotFound

    @staticmethod
    def create(username, password, is_staff=False):
        """Create user"""
        
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
        """Try to log on user using specified username and password"""
        
        assert username and password
        
        fields = {
            'username': username,
            'password': utils.get_hash(password)
        }
        
        user = db.users.find_one(fields)
        
        if user is not None:
            return User(user['username'])
        else:
            raise UserNotFound
        
    @staticmethod
    def objects(fields=None):
        """Get all users from store"""
        
        result = []
        for user in db.users.find():
            result.append(User(user['username']))
        
        return result
