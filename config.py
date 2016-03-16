# -*- coding: utf-8 -*-
# Application config

import redis
from pymongo import MongoClient


SETTINGS = {
    'db_client': MongoClient('mongodb://localhost:27017/'),
    'storage': redis.StrictRedis(host='localhost', port=6379, db=0),
    'debug': True
}


def get(field, default=None):
    return SETTINGS[field] if field in SETTINGS else default
