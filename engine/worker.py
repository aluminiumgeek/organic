# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Worker

import pymongo
from pymongo.errors import InvalidId
from bson.objectid import ObjectId

from engine.database import db


class WorkerNotFound(Exception):
    
    def __str__(self):
        return 'Worker not found'


class Worker(object):
    
    def __init__(self, _id=None, name=None, pin=None):
        if _id is None:
            self.name = name
            self.pin = pin
            
            self._id = str(db.workers.insert({'name': name, 'pin': pin}))
        else:
            try:
                worker = db.workers.find_one({'_id': ObjectId(_id)})
            except InvalidId:
                raise WorkerNotFound
            else:
                if worker is not None:
                    self._id = _id
                    self.name = worker['name']
                    self.pin = worker['pin']
                else:
                    raise WorkerNotFound

    def is_busy(self):
        return db.tasks.find_one({'worker': self.name}) is None

    @staticmethod
    def objects():
        result = []
        for worker in db.workers.find():
            result.append(Worker(str(worker['_id'])))
        
        return result
    