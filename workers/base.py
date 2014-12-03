# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Base worker class

import sys
import signal
import socket
import errno
import json


class RegisterException(Exception):
    """Raises when worker can't register on server"""
    
    pass


class BaseWorker(object):
    """Base worker"""
    
    ACTION_REGISTER = 'register'
    ACTION_UNREGISTER = 'unregister'
    ACTION_RESULT = 'result'
    
    def __init__(self, hostname='localhost', port=1111):
        self.hostname = hostname
        self.port = port
        
        self.worker_id = None
        
        self.__open_socket()
        
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
        
        self.__send(data)
    
        try:
            data = self.__receive(timeout=3)
        except socket.timeout:
            print 'Timed out'
            
            self.__reopen()
            self.register()
            
            return

        if 'worker_id' in data:
            self.worker_id = data['worker_id']
        else:
            raise RegisterException, data

    def unregister(self, stop=True):
        """Unregister this worker from server"""
        
        data = {
            'action': self.ACTION_UNREGISTER,
            'worker_id': self.worker_id
        }
        
        self.__send(data)
        
        try:
            data = self.__receive(timeout=3)
        except socket.timeout:
            self.__reopen()
            self.unregister()
            
            return
        
        if stop:
            self.__stop('Worker is offline')

    def wait(self):
        """Main worker loop. Wait for input tasks"""
        
        print 'Waiting...'
        
        while True:
            data = self.__receive()
            self.__close_socket()
            
            print 'Received ', data
            
            if 'items' in data:
                result = {
                    'action': self.ACTION_RESULT,
                    'result': self.work(data['items']),
                    'worker_id': self.worker_id
                }
                
                self.__result(result)
    
    def work(self):
        """Process data"""
        
        raise NotImplementedError
    
    def __open_socket(self):
        """Open socket"""
        
        self.socket = socket.socket()
        try:
            self.socket.connect((self.hostname, self.port))
        except socket.error, e:
            if e.args[0] == errno.ECONNREFUSED:
                self.__stop('Server is offline')
        
    def __close_socket(self):
        self.socket.close()
        
    def __send(self, data):
        """Send JSON-encoded data"""
        
        self.socket.send(json.dumps(data))

    def __receive(self, size=1024, timeout=None):
        """Receive and decode data"""
        
        try:
            if timeout is not None:
                self.socket.settimeout(timeout)
            # Clear socket timeout
            elif self.socket.gettimeout():
                self.socket.settimeout(None)
            
            data = json.loads(self.socket.recv(size))
        except ValueError:
            self.__stop('Server is offline')
        else:
            return data

    def __result(self, result):
        """Send result to the server"""
        
        print 'Sending ', result
                
        self.__open_socket()
        self.__send(result)
        
        try:
            self.__receive(timeout=2)
        except socket.timeout:
            self.__close_socket()
            self.__result(result)
            
            return
                
        self.__reopen()
        self.unregister(stop=False)
                
        self.__reopen()
        self.register()
        
        print 'End task'

    def __reopen(self):
        """Reopen connection"""
        
        self.__close_socket()
        self.__open_socket()

    def __stop(self, msg=''):
        """Stop this worker"""
        
        print msg
        
        self.__close_socket()
        sys.exit(0)

    def __signal_handler(self, signalnum, _):
        if signalnum == signal.SIGTERM:
            print 'Killing worker...'
            
            self.unregister()
