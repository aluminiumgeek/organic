# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# farm.0x80.ru

from tornado import web, ioloop
from tornado.options import define, options

import database
import config
import handlers

define("port", default=8000, help="run on the given port", type=int)


application = web.Application([
    (r'/user/auth', handlers.AuthHandler),
    (r'/user/create', handlers.UserHandler),
    (r'/tasks', handlers.TasksHandler),
    (r'/workers', handlers.WorkersHandler),
    (r'/task', handlers.TaskHandler),
    (r'/task/(.*)', handlers.TaskHandler),
    (r'/result/(.*)', handlers.ResultHandler),
    
    (r'/(.*)', web.StaticFileHandler, {"path": "public"})
    ],
    debug=config.get('debug', True)
)


if __name__ == "__main__":
    options.parse_command_line()
    application.listen(options.port)
    ioloop.IOLoop.instance().start()
