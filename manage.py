#!/usr/bin/env python
import os
# import unittest

# from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from recyclus_sim import create_app

app = create_app(os.getenv('FLASK_ENV') or 'development')

# app.app_context().push()

manager = Manager(app)

# migrate = Migrate(app, db)

# manager.add_command('db', MigrateCommand)

@manager.command
def run():
    app.run(host='0.0.0.0', port=5010)


if __name__ == '__main__':
    manager.run()
