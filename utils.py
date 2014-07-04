# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Some utils

import hashlib
import uuid

from database import db
from user import User


def get_hash(data):
    return hashlib.sha256(data).hexdigest()


def get_token():
    return str(uuid.uuid4())


def login_required(f):
    def wrapper(handler):
        user = _get_auth_user(handler.request.headers.get('Authorization'))
        
        if user is not None:
            handler.user = user
            return f(handler)
        else:
            handler.finish({
                'status': 'error',
                'msg': 'Login required'
            })
    
    return wrapper


def admin_rights_required(f):
    def wrapper(handler):
        
        user = _get_auth_user(handler.request.headers.get('Authorization'))

        if user is not None and user.is_staff:
            handler.user = user
            return f(handler)
        else:
            handler.finish({
                'status': 'error',
                'msg': 'Admin rights required'
            })
    
    return wrapper


def _get_auth_user(header):
    user = None
    
    if header is not None:
        scheme, _, token= header.partition(' ')
        if scheme.lower() == 'bearer':
            session = db.sessions.find_one({'token': token})
            
            if session is not None:
                user = User(session['username'])

    return user
