# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Worker itself

from base import BaseWorker


class Worker(BaseWorker):
    
    name = 'worker1'
    pin = '1234'


if __name__ == '__main__':
    worker = Worker()
    
    worker.register()
    
    try:
        worker.wait()
    except KeyboardInterrupt:
        print 'Exiting...'
        
        worker.unregister()
