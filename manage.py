#!/usr/bin/env python
import os
# import unittest
from flask_script import Manager

from recyclus_batch import create_app

app = create_app(os.getenv('FLASK_ENV') or 'production')

# app.app_context().push()

manager = Manager(app)


@manager.command
def run():
    app.run(host='0.0.0.0', port=5010)


if __name__ == '__main__':
    manager.run()
