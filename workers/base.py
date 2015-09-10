# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Base worker class

import sys
import signal
import json
import time
import redis


class RegisterException(Exception):
    """Raises when worker can't register on server"""

    pass


class BaseWorker(object):
    """Base worker"""

    ACTION_REGISTER = 'register'
    ACTION_UNREGISTER = 'unregister'
    ACTION_RESULT = 'result'

    def __init__(self, hostname='localhost', port=6379, db):
        self.storage = redis.StrictRedis(host=host, port=port, db=db)

        self.worker_id = None

        self.pubsub = self.storage.pubsub(ignore_subscribe_messages=True)
        self.pubsub.subscribe('tasks')
        
        self.worker_pubsub = self.storage.pubsub(ignore_subscribe_messages=True)
        p.subscribe(workers=self.__cb)
        self.thread = p.run_in_thread(sleep_time=0.6)

        # Catch POSIX SIGTERM signal
        signal.signal(signal.SIGTERM, self.__signal_handler)

    def register(self):
        """Register this worker on server"""

        print 'Registering...'

        data = {
            'action': self.ACTION_REGISTER,
            'name': self.name,
            'pin': self.pin
        }
        self.storage.publish('worker', data)

    def unregister(self, stop=True):
        """Unregister this worker from server"""

        data = {
            'action': self.ACTION_UNREGISTER,
            'worker_id': self.worker_id,
            'pin': self.pin
        }
        self.storage.publish('worker', data)

        if stop:
            self.__stop('Worker is offline')

    def run(self):
        """Main worker loop. Wait for input tasks"""

        print 'Waiting...'

        while True:
            message = self.pubsub.get_message()
            if message['worker_id'] == self.worker_id:
                print 'Received ', message

                result = {
                    'action': self.ACTION_RESULT,
                    'result': self.work(message['data']),
                    'worker_id': self.worker_id,
                    'task_id': message['_id']
                }
                self.storage.publish('tasks', result)
            time.sleep(0.6)

    def work(self):
        """Process data"""

        raise NotImplementedError

    def __cb(self, data):
        name = data.get('name')
        if name == self.name:
            action = data.get('action')
            if action == self.ACTION_REGISTER:
                if 'worker_id' in data:
                    self.worker_id = data['worker_id']
                else:
                    raise RegisterException, data
            elif action == self.ACTION_UNREGISTER:
                pass

    def __stop(self, msg=''):
        """Stop this worker"""

        print msg
        self.thread.stop()
        sys.exit(0)

    def __signal_handler(self, signalnum, _):
        if signalnum == signal.SIGTERM:
            print 'Killing worker...'

            self.unregister()
