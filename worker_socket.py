# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Interaction with workers

import random
import errno
import functools
import socket
import json

from tornado import ioloop

import config
from engine import errors
from engine.worker import Worker, WorkerExists
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
                print 'Worker %s registered'%worker.name
                
                workers.append((worker, connection, address))
                
                result = {
                    'worker_id': worker._id
                }

        elif data['action'] == ACTION_UNREGISTER:
            try:
                worker = Worker(data['worker_id'])
            except WorkerNotFound:
                result = errors.get(errors.WORKER_NOT_FOUND)
            else:
                print 'Worker %s unregistered'%worker.name
                worker.unregister()
                conn.close()
                return
        
        elif data['action'] == ACTION_RESULT:
            try:
                worker = Worker(data['worker_id'])
            except WorkerNotFound:
                result = errors.get(errors.WORKER_NOT_FOUND)
            else:
                print 'Worker %s ending task'%worker.name
                worker.end_task(data['result'])

        connection.send(json.dumps(result))


def send_task(task):
    free_workers = []
    print task._id
    for item in workers:
        worker, connection, _ = item
        
        if not worker.is_busy():
            free_workers.append((worker, connection))

    if free_workers:
        worker, connection = random.choice(free_workers)
        
        print 'Sending task {0} to {1}'.format(task._id, worker.name)
        
        task.set_worker(worker.name)
        
        result = {'items': task.items}
        connection.send(json.dumps(result))


def check_tasks():
    for task in Task.objects({'worker': None, 'result': None}):
        send_task(task)


def connection_ready(sock, fd, events):
    while True:
        try:
            connection, address = sock.accept()
        except socket.error, e:
            if e.args[0] not in (errno.EWOULDBLOCK, errno.EAGAIN):
                raise
        
        connection.setblocking(0)
        handle_connection(connection, address)


def init():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setblocking(0)
    sock.bind(('', config.get('listen_port', 1111)))
    sock.listen(128)

    io_loop = ioloop.IOLoop.instance()
    callback = functools.partial(connection_ready, sock)
    io_loop.add_handler(sock.fileno(), callback, io_loop.READ)
    
    check_tasks_timeout = ioloop.PeriodicCallback(check_tasks, 1000)
    check_tasks_timeout.start()
