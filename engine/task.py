# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Task

import pymongo
from pymongo.errors import InvalidId
from bson.objectid import ObjectId

from engine.database import db


class TaskNotFound(Exception):
    
    def __str__(self):
        return 'Task not found'


class Task(object):
    
    STATUS_WAIT = 1
    STATUS_SUCCESS = 2
    STATUS_ERROR = 3
    
    PRIORITY_LOW = 1
    PRIORITY_NORMAL = 2
    PRIORITY_HIGH = 3
    
    def __init__(self, _id=None, items=[], priority=None):
        if _id is None:
            self.items = items
            self.priority = priority or self.PRIORITY_NORMAL
            self.status = self.STATUS_WAIT
            self.worker = None
            self.result = None
            
            self._id = str(db.tasks.insert({
                'items': self.items,
                'priority': self.priority,
                'status': self.status,
                'worker': self.worker,
                'result': self.result
            }))
        else:
            try:
                task = db.tasks.find_one({'_id': ObjectId(_id)})
            except InvalidId:
                raise TaskNotFound
            else:
                if task is not None:
                    self._id = _id
                    self.items = task['items']
                    self.priority = task['priority']
                    self.status = task['status']
                    self.worker = task['worker']
                    self.result = task['result']
                else:
                    raise TaskNotFound
    
    def set_worker(self, worker):
        self.worker = worker
       
        self.__update_field('worker', worker)
        
    def set_status(self, status):
        self.status = status
        
        self.__update_field('status', status)

    def set_result(self, result):
        self.result = result
        
        self.__update_field('result', result)

    def save_result(self, result):
        self.set_status = STATUS_SUCCESS
        self.set_result(result)
        self.set_worker = None

    @staticmethod
    def objects():
        result = []
        for task in db.tasks.find():
            result.append(Task(str(task['_id'])))
        
        return result

    def __update_field(self, name, value):
        db.tasks.update(
            {'_id': self._id}, 
            {"$set": {name: value}}
        )
