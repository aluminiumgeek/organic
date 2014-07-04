# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Some utils

import hashlib
import uuid


def get_hash(data):
    return hashlib.sha256(data).hexdigest()


def get_token():
    return str(uuid.uuid4())
