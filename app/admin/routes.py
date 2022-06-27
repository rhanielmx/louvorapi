from app import app
from flask import Blueprint, request
from flask_restx import Resource, Api, fields

from app.models import Category, Song

admin_bp = Blueprint('admin',__name__)

api = Api(admin_bp)
