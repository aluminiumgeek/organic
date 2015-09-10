# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Some utils

import hashlib
import uuid

from engine.database import db
from engine.user import User
from engine import errors


def get_hash(data):
    """Returns hashed string"""

    return hashlib.sha256(data).hexdigest()


def get_token():
    return str(uuid.uuid4())


def login_required(f):
    """Decorator checks user authentication"""

    def wrapper(handler):
        user = _get_auth_user(handler.request.headers.get('Authorization'))

        if user is not None:
            handler.user = user
            return f(handler)
        else:
            handler.finish(errors.get(errors.LOGIN_REQUIRED))

    return wrapper


def admin_rights_required(f):
    """Decorator checks user authentication and admin rights"""

    def wrapper(handler):

        user = _get_auth_user(handler.request.headers.get('Authorization'))

        if user is not None and user.is_staff:
            handler.user = user
            return f(handler)
        else:
            handler.finish(errors.get(errors.ADMIN_RIGHTS_REQUIRED))

    return wrapper


def _get_auth_user(header):
    """Try to get user by token"""

    user = None

    if header is not None:
        scheme, _, token= header.partition(' ')
        if scheme.lower() == 'bearer':
            session = db.sessions.find_one({'token': token})

            if session is not None:
                user = User(session['username'])

    return user
