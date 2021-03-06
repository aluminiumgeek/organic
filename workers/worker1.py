# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Typical worker structure. Example.

from base import BaseWorker


class Worker(BaseWorker):

    name = 'worker1'
    pin = '1234'

    def work(self, data):
        import time
        import hashlib

        result = hashlib.md5(str(data)).hexdigest()

        time.sleep(10)

        return result


if __name__ == '__main__':
    worker = Worker()
    worker.register()

    try:
        worker.run()
    except KeyboardInterrupt:
        print 'Exiting...'
        worker.unregister()
