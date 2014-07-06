# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Base worker class

import time
import sys
import socket
import errno
import json


class RegisterException(Exception):
    pass


class BaseWorker(object):
    
    ACTION_REGISTER = 'register'
    ACTION_UNREGISTER = 'unregister'
    ACTION_RESULT = 'result'
    
    def __init__(self, hostname='localhost', port=1111):
        self.hostname = hostname
        self.port = port
        
        self.__open_socket()

    def register(self):
        data = {
            'action': self.ACTION_REGISTER,
            'name': self.name,
            'pin': self.pin
        }
        
        self.__send(data)
    
        data = self.__receive()

        if 'worker_id' in data:
            self.worker_id = data['worker_id']
        else:
            raise RegisterException, data

    def unregister(self):
        data = {
            'action': self.ACTION_UNREGISTER,
            'worker_id': self.worker_id
        }
        
        self.__send(data)

    def wait(self):
        print 'Waiting...'
        
        while True:
            data = self.__receive()
            self.__close_socket()
            
            print 'Received ', data
            
            if 'items' in data:
                result = {
                    'action': self.ACTION_RESULT,
                    'result': self.work(len(data['items'])),
                    'worker_id': self.worker_id
                }
                
                self.__result(result)
    
    def work(self, t):
        time.sleep(t)
        
        return t, time.time()
        
    def __open_socket(self):
        self.socket = socket.socket()
        try:
            self.socket.connect((self.hostname, self.port))
        except socket.error, e:
            if e.args[0] == errno.ECONNREFUSED:
                self.__stop('Server is offline')
        
    def __close_socket(self):
        self.socket.close()
        
    def __send(self, data):
        self.socket.send(json.dumps(data))

    def __receive(self, size=1024, timeout=None):
        try:
            if timeout is not None:
                self.socket.settimeout(2)
            
            data = json.loads(self.socket.recv(size))
        except ValueError:
            self.__stop('Server is offline')
        else:
            return data

    def __result(self, result):
        print 'Sending ', result
                
        self.__open_socket()
        self.__send(result)
        
        try:
            self.__receive(timeout=2)
        except socket.timeout:
            self.__close_socket()
            self.__result(result)
                
        self.__reopen()
                
        self.unregister()
                
        self.__reopen()
        
        self.register()
        
        print 'Task end'

    def __reopen(self):
        self.__close_socket()
        self.__open_socket()

    def __stop(self, msg):
        print msg
        
        self.__close_socket()
        sys.exit(1)
