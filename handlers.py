# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Handlers

import json
import motor

from tornado import web, gen

import config
import utils
import errors


class AuthHandler(web.RequestHandler):
    
    @web.asynchronous
    @gen.engine
    def post(self):
        params = json.loads(self.request.body)

        params['password'] = utils.get_hash(params['password'])

        user = yield motor.Op(config['db'].users.find_one, **params)
        
        if user is not None:
            token = utils.get_token()
            
            session = {
                'user': user['_id'],
                'token': token
            }
            
            yield motor.Op(config.get('db').sessions.insert, session)
            
            data = {
                'username': user['username'],
                'is_staff': user['is_staff']
            }
        else:
            data = errors.USER_NOT_FOUND
            
        self.finish(data)


class UserHandler(web.RequestHandler):
    
    @web.asynchronous
    @gen.engine
    def post(self):
        """Create user"""
        
        params = json.loads(self.request.body)
        
        params['password'] = utils.get_hash(params['password'])
        
        yield motor.Op(config.get('db').users.insert, params)

        self.finish()