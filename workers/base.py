# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Base worker class

import time
import socket
import json


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
            print data

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
                    'result': self.work(len(data['items']))
                }
                
                print 'Sending ', data
                
                self.__open_socket()
                self.__send(data)

    def work(self, t):
        time.sleep(t)
        
        return t, time.time()
        
    def __open_socket(self):
        self.socket = socket.socket()
        self.socket.connect((self.hostname, self.port))
        
    def __close_socket(self):
        self.socket.close()
        
    def __send(self, data):
        self.socket.send(json.dumps(data))

    def __receive(self, size=1024):
        return json.loads(self.socket.recv(size))