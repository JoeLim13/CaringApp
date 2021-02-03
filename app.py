import os
import config
from flask import Flask
from models.base_model import db
from apscheduler.schedulers.background import BackgroundScheduler

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'caringapp_web')

app = Flask('CARINGAPP', root_path=web_dir)
app.secret_key = os.getenv("SECRET_KEY")

scheduler = BackgroundScheduler()

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc
