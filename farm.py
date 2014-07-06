# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# farm.0x80.ru

from tornado import web, ioloop
from tornado.options import define, options

import config
import handlers
import worker_socket


define("port", default=8000, help="run on the given port", type=int)


application = web.Application([
    (r'/api/user/auth', handlers.AuthHandler),
    (r'/api/user/create', handlers.UserHandler),
    (r'/api/tasks', handlers.TasksHandler),
    (r'/api/workers', handlers.WorkersHandler),
    (r'/api/task', handlers.TaskHandler),
    (r'/api/task/(.*)', handlers.TaskHandler),
    (r'/api/result/(.*)', handlers.ResultHandler),
    
    (r'/(.*)', web.StaticFileHandler, {"path": "web"})
    ],
    debug=config.get('debug', True)
)


if __name__ == "__main__":
    options.parse_command_line()
    application.listen(options.port)
    worker_socket.init()
    
    ioloop.IOLoop.instance().start()
