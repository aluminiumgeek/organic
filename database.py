# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Database schemes and callbacks

import config

user_schema = {
    'username': '',
    'password': '',
    'is_staff': False
}

worker_schema = {
    'name': '',
    'pin': ''
}

task_schema = {
    'items': [],
    'status': 0,
    'priority': 0,
    'worker': ''
}

session_schema = {
    'username': '',
    'token': ''
}


db = config.get('db_client').farm


def insert_callback(result, error):
    if error:
        raise error
