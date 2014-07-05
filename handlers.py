# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Handlers

import json

from tornado import web, gen

import utils
import errors
from database import db
from user import User, UserNotFound, UsernameExists
from task import Task, TaskNotFound
from worker import Worker, WorkerNotFound


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
    
    @utils.login_required
    def delete(self):
        """Revoke token and logout"""
        
        db.sessions.remove({'username': self.user.username})


class UserHandler(web.RequestHandler):

    @utils.admin_rights_required
    def post(self):
        """Create user"""
        
        username = self.get_argument('username').strip()
        password = self.get_argument('password').strip()
        is_staff = True if self.get_argument('is_staff') == '1' else False
        
        try:
            User.create(username, password, is_staff)
        except UsernameExists:
            data = errors.get(errors.USERNAME_EXISTS)
        else:
            data = {
                'status': 'ok'
            }

        self.finish(data)

class TaskHandler(web.RequestHandler):
    
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
    
    def post(self):
        """Register task"""
        
        body = json.loads(self.request.body)
        
        if 'items' in body and body['items']:
            task = Task(items=body['items'], priority=body['priority'])
            data = {
                'status': 'ok',
                'task_id': task._id
            }
        else:
            data = errors.get(error.TASK_NO_ITEMS)
        
        self.finish(data)


class ResultHandler(web.RequestHandler):
    
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
