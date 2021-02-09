from app import app, csrf
from flask_cors import CORS

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

## API Routes ##
from caringapp_api.blueprints.users.views import users_api_blueprint
from caringapp_api.blueprints.schemes.views import schemes_api_blueprint
from caringapp_api.blueprints.sessions.views import sessions_api_blueprint


csrf.exempt(users_api_blueprint)
csrf.exempt(sessions_api_blueprint)
csrf.exempt(schemes_api_blueprint)
app.register_blueprint(users_api_blueprint, url_prefix='/api/v1/users')
app.register_blueprint(schemes_api_blueprint, url_prefix='/api/v1/schemes')
app.register_blueprint(sessions_api_blueprint, url_prefix ='/api/v1/sessions')
