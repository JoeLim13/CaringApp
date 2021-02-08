from app import app, scheduler
from flask import render_template
from caringapp_web.blueprints.users.views import users_blueprint
from caringapp_web.blueprints.schemes.views import schemes_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from datetime import time, date
from caringapp_web.blueprints.sessions.views import sessions_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from caringapp_web.util.google_oauth import oauth

assets = Environment(app)
assets.register(bundles)

oauth.init_app(app)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(schemes_blueprint, url_prefix="/schemes")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(404)
def page_no_found(e):
    return render_template('404.html'), 404


@app.route("/")
def home():
    return render_template('home.html')

# @scheduler.task('interval', id='do_job_1', seconds=5)
# def job1():
#    print('Job 1 executed')
