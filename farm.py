# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# farm.0x80.ru

from tornado import web, ioloop
from tornado.options import define, options

import config
import handlers
import orihara


define("port", default=8000, help="run on the given port", type=int)

application = web.Application([
    (r'/api/user/auth', handlers.AuthHandler),
    (r'/api/tasks', handlers.TasksHandler),
    (r'/api/workers', handlers.WorkersHandler),
    (r'/api/users', handlers.UsersHandler),
    (r'/api/task', handlers.TaskHandler),
    (r'/api/task/(.*)', handlers.TaskHandler),
    (r'/api/result/(.*)', handlers.ResultHandler)
    ],
    debug=config.get('debug', True)
)


if __name__ == "__main__":
    options.parse_command_line()
    application.listen(options.port)
    orihara.init()
    ioloop.IOLoop.instance().start()
