# -*- coding: utf-8 -*-
# Pub/sub implementation over redis for interaction with workers 

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


def send_task(task):
    """Sends task to random free worker"""

    free_workers = []

    for item in workers:
        if not item.is_busy():
            free_workers.append(item)

    if free_workers:
        free_worker = random.choice(free_workers)
        print 'Sending task {0} to {1}'.format(
            task._id, 
            free_worker.name
        )

        task.set_worker(free_worker.name)

        result = {
            '_id': task._id,
            'data': task.data,
            'worker_id': free_worker._id,
            'direction': 'workers'
        }
        
        config.get('storage').publish(Task.CHANNEL, json.dumps(result))


def check_tasks():
    """Check uncompleted tasks"""

    for task in Task.objects({'worker': None, 'result': None}):
        send_task(task)


def handle_worker(message):
    data = json.loads(message.get('data', '{}'))

    if data.get('direction') != __name__:
        return

    action = data.get('action')
    result = {}

    if action == ACTION_REGISTER:
        try:
            worker = Worker(name=data['name'], pin=data['pin'])
        except WorkerExists:
            result = errors.get(errors.WORKER_EXISTS)
        else:
            worker.release()
            workers.append(worker)

            result = {
                'action': action,
                'name': data['name'],
                'worker_id': worker._id,
                'direction': 'workers'
            }

            print '{} joined'.format(data['name'])

    elif action == ACTION_UNREGISTER:
        try:
            worker = Worker(data['worker_id'], pin=data['pin'])
        except WorkerNotFound:
            result = errors.get(errors.WORKER_NOT_FOUND)
        else:
            worker.unregister()

            result = {
                'action': action,
                'worker_id': worker._id,
                'direction': 'workers'
            }

            for w in filter(lambda x: x.name == worker.name, workers):
                workers.remove(w)

            print '{} left'.format(worker.name)

    if result:
        config.get('storage').publish(Worker.CHANNEL, json.dumps(result))


def handle_task(message):
    data = json.loads(message.get('data', '{}'))
    action = data.get('action')

    if action == ACTION_RESULT:
        try:
            worker = Worker(data['worker_id'], pin=data['pin'])
        except WorkerNotFound:
            result = errors.get(errors.WORKER_NOT_FOUND)
        else:
            worker.end_task(data['result'])


def init():
    storage = config.get('storage')
    pubsub = storage.pubsub(ignore_subscribe_messages=True)
    channels = {Task.CHANNEL: handle_task, Worker.CHANNEL: handle_worker}
    pubsub.subscribe(**channels)
    pubsub.run_in_thread(sleep_time=0.6)

    # Check for new tasks every 600 ms
    check_tasks_timeout = ioloop.PeriodicCallback(check_tasks, 600)
    check_tasks_timeout.start()
