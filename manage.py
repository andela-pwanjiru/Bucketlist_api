import os

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from api import app, db, config


app.config.from_object(config.DevelopmentConfig)


migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
