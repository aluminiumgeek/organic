# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Base worker class

import sys
import signal
import json
import time
import redis


class BaseWorker(object):
    """Base worker"""

    ACTION_REGISTER = 'register'
    ACTION_UNREGISTER = 'unregister'
    ACTION_RESULT = 'result'

    def __init__(self, hostname='localhost', port=6379, db=0):
        self.storage = redis.StrictRedis(host=hostname, port=port, db=db)

        self.worker_id = None

        self.pubsub = self.storage.pubsub(ignore_subscribe_messages=True)
        self.pubsub.subscribe('tasks')

        self.worker_pubsub = self.storage.pubsub(ignore_subscribe_messages=True)
        self.worker_pubsub.subscribe(workers=self.__cb)
        self.thread = self.worker_pubsub.run_in_thread(sleep_time=0.3)

        # Catch POSIX SIGTERM signal
        signal.signal(signal.SIGTERM, self.__signal_handler)

    def register(self):
        """Register this worker on server"""

        print 'Registering...'

        data = {
            'action': self.ACTION_REGISTER,
            'name': self.name,
            'pin': self.pin,
            'direction': 'orihara'
        }
        self.storage.publish('workers', json.dumps(data))

    def unregister(self):
        """Unregister this worker from server"""

        data = {
            'action': self.ACTION_UNREGISTER,
            'worker_id': self.worker_id,
            'pin': self.pin,
            'direction': 'orihara'
        }
        self.storage.publish('workers', json.dumps(data))

    def run(self):
        """Main worker loop. Wait for input tasks"""

        print 'Waiting...'

        while True:
            message = self.pubsub.get_message()

            if message is None:
                continue

            data = json.loads(message.get('data', '{}'))
            if data.get('direction') == 'workers' and data.get('worker_id') == self.worker_id:
                print 'Received task {} with data: {}'.format(data['_id'], data['data'])

                work_result = self.work(data['data'])
                result = {
                    'action': self.ACTION_RESULT,
                    'result': work_result,
                    'worker_id': self.worker_id,
                    'pin': self.pin,
                    'task_id': data['_id'],
                    'direction': 'orihara'
                }
                print 'Task {} success with result: {}'.format(data['_id'], work_result)

                self.storage.publish('tasks', json.dumps(result))
            time.sleep(0.6)

    def work(self):
        """Process data"""

        raise NotImplementedError

    def __cb(self, message):
        if message is not None:
            data = json.loads(message.get('data', '{}'))
            name = data.get('name')

            if data.get('direction') == 'workers':
                action = data.get('action')
                worker_id = data.get('worker_id')
                if action == self.ACTION_REGISTER and worker_id is not None and data.get('name') == self.name:
                    self.worker_id = worker_id
                elif action == self.ACTION_UNREGISTER and worker_id == self.worker_id:
                    self.__stop('Worker is offline')

    def __stop(self, msg=''):
        """Stop this worker"""

        print msg
        #self.thread.stop()
        self.worker_pubsub.unsubscribe()
        sys.exit(0)

    def __signal_handler(self, signalnum, _):
        if signalnum == signal.SIGTERM:
            print 'Killing worker...'

            self.unregister()
