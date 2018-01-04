Organic
=============

Distributed task farming system with RESTful API, authentication and web interface.  
Demo version: http://farm.0x80.ru (username & password: admin)


## Requirements
* [MongoDB](http://www.mongodb.org)
* [Redis](http://redis.io)


## API methods
Note: user token must be sent with Authorization header:  
<code>Authorization: Bearer &lt;token&gt;</code>

<code>POST /api/user/auth</code>  
Authenticate user, create session and return token.  
Parameters: username, password

<code>POST /api/users</code>  
Create new user.  
Parameters: username, password, is_staff

<code>GET /api/users</code>  
Get list of users.

<code>GET /api/tasks</code>  
Get list of tasks.

<code>GET /api/workers</code>  
Get list of workers.

<code>POST /api/task</code>  
Create task.  
Parameters (JSON encoded): items (list), priority

<code>GET /api/task/:task_id</code>  
Get task status.

<code>GET /api/result/:task_id</code>  
Get task result.
