# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Database schemes and callbacks

import config

users = {
    'username': '',
    'password': '',
    'is_staff': False
}

worker = {
    'name': '',
    'pin': ''
}

tasks = {
    'data': [],
    'status': 0,
    'priority': 0,
    'worker': ''
}

sessions = {
    'username': '',
    'token': ''
}


db = config.get('db_client').farm


def insert_callback(result, error):
    if error:
        raise error
