# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Application config

from pymongo import MongoClient


SETTINGS = {
    'db_client': MongoClient('mongodb://localhost:27017/'),
    'debug': True
}


def get(field, default=None):
    return SETTINGS[field] if field in SETTINGS else default
