# -*- coding: utf-8 -*-
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
    """Class implements worker object"""

    CHANNEL = 'workers'

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

                    if pin is not None and pin != self.pin:
                        raise WorkerNotFound
                else:
                    raise WorkerNotFound

    def is_busy(self):
        """Returns True if there's task on this worker"""

        return db.tasks.find_one({'worker': self.name, \
            'status': Task.STATUS_WAIT}) is not None

    def end_task(self, result):
        """End task and save result"""

        task = db.tasks.find_one({'worker': self.name, 'status': Task.STATUS_WAIT})

        if task is not None:
            task = Task(str(task['_id']))
            task.save_result(result)
        self.release()

    def release(self):
        """Detach worker from all pending task"""

        for task in db.tasks.find({'worker': self.name, 'status': Task.STATUS_WAIT}):
            task = Task(str(task['_id']))
            task.set_worker(None)

    def unregister(self):
        """Remove this worker from store"""

        self.release()
        db.workers.remove({'name': self.name})

    @staticmethod
    def objects(fields=None):
        """Get all workers from store"""

        result = []
        for worker in db.workers.find():
            result.append(Worker(str(worker['_id'])))

        return result

    def __db_to_attrib(self, db_item):
        self._id = str(db_item['_id'])
        self.name = db_item['name']
        self.pin = db_item['pin']
