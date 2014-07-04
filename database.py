# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Database schemes and callbacks

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
    'user': '',
    'token': ''
}


def insert_callback(result, error):
    if error:
        raise error
