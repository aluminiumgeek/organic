# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Application config

from pymongo import MongoClient


SETTINGS = {
    'db_client': MongoClient('mongodb://localhost:27017/'),
    'listen_port': 1111, # listen for worker connections
    'debug': True
}


def get(field, default=None):
    return SETTINGS[field] if field in SETTINGS else default
