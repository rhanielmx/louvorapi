from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, \
                               unset_jwt_cookies, jwt_required, JWTManager

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from pytz import utc
from datetime import datetime

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

from app.users.models import User

def func():
    users = User.query.all()
    for user in users:
        user.role = 'user'
        user.update(user.username, user.email, user.password, user.first_name, user.last_name, user.role)
        print(f'hello from {user.username} cargo {user.role} at {utc.localize(datetime.now())}')

jobstores = {
    # 'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
    'default': SQLAlchemyJobStore(url=Config.SQLALCHEMY_DATABASE_URI)
}

executors = {
    'default': ThreadPoolExecutor(20),
}

job_defaults = {
    'coalesce': False,
    'max_instances': 1
}

scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)
scheduler.add_job(func, 'cron', id='func', replace_existing=True, year='*', month='*', day='last', hour='23', minute='59', second='59') # seconds=30, misfire_grace_time=None, )
scheduler.start()