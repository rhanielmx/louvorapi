from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, \
                               unset_jwt_cookies, jwt_required, JWTManager

from config import Config

app = Flask(__name__)
CORS(app)

app.config.from_object(Config)
jwt = JWTManager(app)
db = SQLAlchemy(app)

Migrate(app,db)

from app.admin.routes import admin_bp
from app.handler.routes import handler_bp
from app.users.routes import users_bp

app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(handler_bp, url_prefix='/handler')
app.register_blueprint(users_bp, url_prefix='/user')
