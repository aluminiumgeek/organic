# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# List of API errors

USER_NOT_FOUND = (1, 'User not found')
INVALID_LOGIN = (2, 'Invalid username or password')
USERNAME_EXISTS = (3, 'Username exists')
TASK_NOT_FOUND = (4, 'Task not found')
TASK_NO_ITEMS = (5, 'No job(s) specified')

WORKER_EXISTS = (6, 'Worker exists, try another name')
WORKER_NOT_FOUND = (7, 'Worker not found')

BAD_PASSWORD = (8, 'Bad password')

LOGIN_REQUIRED = (9, 'Login required')
ADMIN_RIGHTS_REQUIRED = (10, 'Admin rights required')

INCORRECT_PRIORITY = (11, 'Incorrect priority value')


def get(error):
    code, msg = error
    
    return {
        'status': 'error',
        'code': code,
        'msg': msg
    }
