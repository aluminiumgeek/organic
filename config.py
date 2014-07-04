# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Application config

import motor

SETTINGS = {
    'db': motor.MotorClient().open_sync().farm,
    'debug': True
}

def get(field, default=None):
    return SETTINGS[field] if field in SETTINGS else default
