import os
from flask.ext.script import Manager
from texter import app
from getpass import getpass
from werkzeug.security import generate_password_hash
from flask.ext.migrate import Migrate, MigrateCommand
from texter.database import Base, session, Notification
from texter.text import send_text
from apscheduler.schedulers.blocking import BlockingScheduler

manager = Manager(app)

@manager.command
def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
    
@manager.command
def schedule_task():
    
    sched = BlockingScheduler()
    @sched.scheduled_job('interval', hours=1)
    def timed_job():
        notifications = session.query(Notification).all()
        for n in notifications:
            send_text(n)
        print("ran job")
    sched.start()
    
class DB(object):
    def __init__(self, metadata):
        self.metadata = metadata

migrate = Migrate(app, DB(Base.metadata))
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()