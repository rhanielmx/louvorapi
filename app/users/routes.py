from app import app, db
from flask import Blueprint, request
from flask_restx import Resource, Api, fields

from app.users.models import User

users_bp = Blueprint('user',__name__)
api = Api(users_bp)