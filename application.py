#!/usr/bin/env python

import os
from app import create_app
from flask.ext.script import Manager, Server

application = create_app(
    os.getenv('NOTIFY_ENVIRONMENT') or 'development'
)
manager = Manager(application)
manager.add_command("runserver", Server(port=6002))

if __name__ == '__main__':
    manager.run()
