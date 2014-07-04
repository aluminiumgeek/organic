# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Handlers

import json

from tornado import web, gen

import config
import utils
import errors
from user import User, UsernameExists


class AuthHandler(web.RequestHandler):

    def post(self):
        params = json.loads(self.request.body)

        params['password'] = utils.get_hash(params['password'])

        user = None
        
        if user is not None:
            token = utils.get_token()
            
            session = {
                'user': user['_id'],
                'token': token
            }
            
            # add session here
            
            data = {
                'username': user['username'],
                'is_staff': user['is_staff']
            }
        else:
            data = errors.USER_NOT_FOUND
            
        self.finish(data)


class UserHandler(web.RequestHandler):

    @utils.admin_rights_required
    def post(self):
        """Create user"""
        
        username = self.get_argument('username').strip()
        password = self.get_argument('password').strip()
        
        try:
            User.create(username, password)
        except UsernameExists:
            raise

        self.finish()


