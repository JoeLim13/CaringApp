from app import app, scheduler
from flask import render_template
from caringapp_web.blueprints.users.views import users_blueprint
from caringapp_web.blueprints.schemes.views import schemes_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(schemes_blueprint, url_prefix="/schemes")

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route("/")
def home():
    return render_template('home.html')

def scheduledTask():
    print("Hello")
    
  
job = scheduler.add_job(scheduledTask, 'interval', minutes=1)
job.start(paused=False)

