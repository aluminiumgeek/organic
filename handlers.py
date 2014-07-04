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


class AuthHandler(web.RequestHandler):

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        
        try: 
            user = User.logon(username, password)
        except UserNotFound:
            data = {
                'status': 'error',
                'msg': 'Invalid username or password'
            }
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
            data = {
                'status': 'error',
                'msg': 'Username exists'
            }
        else:
            data = {
                'status': 'ok'
            }

        self.finish(data)
