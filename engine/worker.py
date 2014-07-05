# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Worker

import pymongo
from pymongo.errors import InvalidId
from bson.objectid import ObjectId

from engine.database import db
from engine.task import Task


class WorkerNotFound(Exception):
    
    def __str__(self):
        return 'Worker not found'


class WorkerExists(Exception):
    
    def __str__(self):
        return 'Worker exists'


class Worker(object):
    
    def __init__(self, _id=None, name=None, pin=None):
        if _id is None:
            if db.workers.find_one({'name': name}) is None:
                self.name = name
                self.pin = pin
            
                self._id = str(db.workers.insert({'name': name, 'pin': pin}))
                
            elif db.workers.find_one({'name': name, 'pin': pin}) is not None:
                self.__db_to_attrib(db.workers.find_one({'name': name, 'pin': pin}))
                
            else:
                raise WorkerExists
        else:
            try:
                worker = db.workers.find_one({'_id': ObjectId(_id)})
            except InvalidId:
                raise WorkerNotFound
            else:
                if worker is not None:
                    self.__db_to_attrib(worker)
                else:
                    raise WorkerNotFound

    def is_busy(self):
        return db.tasks.find_one({'worker': self.name, \
            'status': Task.STATUS_WAIT}) is not None

    def end_task(self, result):
        task = db.tasks.find_one({'worker': self.name})
        
        if task is not None:
            task.save_result(result)
    
    def unregister(self):
        db.tasks.update(
            {'worker': self.name}, 
            {'$set', {'worker': None}}, 
            upsert=False
        )
        
        db.workers.remove({'name': self.name})

    @staticmethod
    def objects(fields=None):
        result = []
        for worker in db.workers.find():
            result.append(Worker(str(worker['_id'])))
        
        return result
    
    def __db_to_attrib(self, db_item):
        self._id = str(db_item['_id'])
        self.name = db_item['name']
        self.pin = db_item['pin']
