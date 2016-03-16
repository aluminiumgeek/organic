# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Handlers

import json

from tornado import web, gen

import utils
from decorators import login_required, admin_rights_required
from engine import errors
from engine.database import db
from engine.user import User, UserNotFound, UsernameExists
from engine.task import Task, TaskNotFound
from engine.worker import Worker, WorkerNotFound


class AuthHandler(web.RequestHandler):

    def post(self):
        """Authenticate and get token"""

        username = self.get_argument('username')
        password = self.get_argument('password')

        try: 
            user = User.logon(username, password)
        except UserNotFound:
            data = errors.get(errors.INVALID_LOGIN)
        else:
            token = utils.get_token()

            session = {
                'username': username,
                'token': token
            }

            db.sessions.insert(session)

            data = {
                'username': username,
                'is_staff': user.is_staff,
                'token': token
            }

        self.finish(data)

    @login_required
    def delete(self):
        """Revoke token and logout"""

        db.sessions.remove({'username': self.user.username})


class TaskHandler(web.RequestHandler):

    @login_required
    def get(self, task_id):
        """Task status"""

        try:
            task = Task(task_id)
        except TaskNotFound:
            data = errors.get(errors.TASK_NOT_FOUND)
        else:
            data = {
                'status': 'ok',
                'result': task.status
            }

        self.finish(data)

    @login_required
    def post(self):
        """Register task"""

        body = json.loads(self.request.body)

        if body.get('data') is not None:
            priority = body.get('priority', Task.PRIORITY_NORMAL)

            if priority in Task.PRIORITIES:
                task = Task.create(data=body['data'], priority=priority)
                data = {
                    'status': 'ok',
                    'task_id': task._id
                }
            else:
                data = errors.get(errors.INCORRECT_PRIORITY)
        else:
            data = errors.get(errors.TASK_NO_DATA)

        self.finish(data)


class ResultHandler(web.RequestHandler):

    @login_required
    def get(self, task_id):
        """Task result"""

        try:
            task = Task(task_id)
        except TaskNotFound:
            data = errors.get(TASK_NOT_FOUND)
        else:
            data = {
                'status': 'ok',
                'result': task.result
            }

        self.finish(data)


class TasksHandler(web.RequestHandler):

    @login_required
    def get(self):
        """List all tasks"""

        tasks = []

        for task in Task.objects():
            tasks.append({
                '_id': task._id,
                'priority': task.priority,
                'status': task.status,
                'worker': task.worker,
                'result': task.result
            })

        self.finish({
            'tasks': tasks
        })


class WorkersHandler(web.RequestHandler):

    @login_required
    def get(self):
        """List all workers"""

        workers = []

        for worker in Worker.objects():
            workers.append({
                'name': worker.name,
                'pin': worker.pin,
                'is_busy': worker.is_busy()
            })

        self.finish({
            'workers': workers
        })


class UsersHandler(web.RequestHandler):

    @admin_rights_required
    def get(self):
        """List all users"""

        users = []

        for user in User.objects():
            users.append({
                'username': user.username,
                'is_staff': user.is_staff,
            })

        self.finish({
            'users': users
        })

    @admin_rights_required
    def post(self):
        """Create user"""

        username = self.get_argument('username').strip()
        password = self.get_argument('password').strip()
        is_staff = True if self.get_argument('is_staff') == '1' else False

        try:
            User.create(username, password, is_staff)
        except UsernameExists:
            data = errors.get(errors.USERNAME_EXISTS)
        except UnicodeEncodeError:
            data = errors.get(errors.BAD_PASSWORD)
        else:
            data = {
                'status': 'ok'
            }

        self.finish(data)
