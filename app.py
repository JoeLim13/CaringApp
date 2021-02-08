import os
import config
from flask import Flask
from flask_apscheduler import APScheduler
from models.base_model import db
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from models.user import User

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'caringapp_web')

app = Flask('CARINGAPP', root_path=web_dir)
csrf = CSRFProtect(app)
jwt = JWTManager(app)
app.secret_key = os.getenv("SECRET_KEY")

scheduler = APScheduler()

# @scheduler.task('cron', id='do_job_1', hour='16', minute='23', second='0')
# def job1():
#    print('Job 1 executed')


scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()


if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view ="sessions.new"
login_manager.login_message= "Please log in before proceeding"
login_manager.login_message_category ="warning"

@login_manager.user_loader
def load_user(user_id):
    return User.get_or_none(User.id == user_id)

@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc
