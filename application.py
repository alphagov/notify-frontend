#!/usr/bin/env python

import os
from app import create_app
from flask.ext.script import Manager, Server

application = create_app(
    os.getenv('NOTIFY_ENVIRONMENT') or 'development'
)
manager = Manager(application)
port = int(os.environ.get('PORT', 6002))
manager.add_command("runserver", Server(host='0.0.0.0', port=port))

if __name__ == '__main__':
    manager.run()
