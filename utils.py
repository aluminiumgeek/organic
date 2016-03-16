# -*- coding: utf-8 -*-
# Some utils

import hashlib
import uuid


def get_hash(data):
    """Returns hashed string"""

    return hashlib.sha256(data).hexdigest()


def get_token():
    return str(uuid.uuid4())
