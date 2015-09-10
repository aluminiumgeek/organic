# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Non-blocking socket for interaction with workers

import random
import errno
import functools
import socket
import json

from tornado import ioloop

import config
from engine import errors
from engine.worker import Worker, WorkerNotFound, WorkerExists
from engine.task import Task


ACTION_REGISTER = 'register'
ACTION_UNREGISTER = 'unregister'
ACTION_RESULT = 'result'


workers = []


def handle_connection(connection, address):

    data = connection.recv(1024)

    if data:
        data = json.loads(data)

        result = {'status': 'ok'}

        if data['action'] == ACTION_REGISTER:
            try:
                worker = Worker(name=data['name'], pin=data['pin'])
            except WorkerExists:
                result = errors.get(errors.WORKER_EXISTS)
            else:
                workers.append({
                    'worker': worker,
                    'connection': connection
                })

                result = {
                    'worker_id': worker._id
                }

        elif data['action'] == ACTION_UNREGISTER:
            try:
                worker = Worker(data['worker_id'])
            except WorkerNotFound:
                result = errors.get(errors.WORKER_NOT_FOUND)
            else:
                worker.unregister()

                for w in filter(lambda x: x['worker'].name == worker.name, workers):
                    workers.remove(w)

                #connection.close()
                #return

        elif data['action'] == ACTION_RESULT:
            try:
                worker = Worker(data['worker_id'])
            except WorkerNotFound:
                result = errors.get(errors.WORKER_NOT_FOUND)
            else:
                worker.end_task(data['result'])

        connection.send(json.dumps(result))


def handle_worker_action(data):
    data = json.loads(data)
    action = data.get('action')

    result = None

    if action == ACTION_REGISTER:
        try:
            worker = Worker(name=data['name'], pin=data['pin'])
        except WorkerExists:
            result = errors.get(errors.WORKER_EXISTS)
        else:
            workers.append({
                'worker': worker,
                'connection': connection
            })

            result = {
                'worker_id': worker._id
            }

    elif action == ACTION_UNREGISTER:
        try:
            worker = Worker(data['worker_id'])
        except WorkerNotFound:
            result = errors.get(errors.WORKER_NOT_FOUND)
        else:
            worker.unregister()

        for w in filter(lambda x: x['worker'].name == worker.name, workers):
            workers.remove(w)


def send_task(task):
    """Sends task to random free worker"""

    free_workers = []

    for item in workers:
        if not item['worker'].is_busy():
            free_workers.append(item)

    if free_workers:
        free_worker = random.choice(free_workers)

        print 'Sending task {0} to {1}'.format(
            task._id, 
            free_worker['worker'].name
        )

        task.set_worker(free_worker['worker'].name)

        result = {'items': task.items}
        free_worker['connection'].send(json.dumps(result))


def check_tasks():
    """Check uncompleted tasks"""

    for task in Task.objects({'worker': None, 'result': None}):
        send_task(task)

def handle_worker(data):
    

def handle_task(data):
    print data


def init():
    storage = config.get('storage')
    pubsub = storage.pubsub()
    pubsub.subscribe(**{Task.CHANNEL: handle_task, Worker.CHANNEL: handle_worker})
    p.run_in_thread(sleep_time=0.6)

    # Check for new tasks every second
    #check_tasks_timeout = ioloop.PeriodicCallback(check_tasks, 1000)
    #check_tasks_timeout.start()
