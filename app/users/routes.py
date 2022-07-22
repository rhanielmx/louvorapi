from flask_jwt_extended import get_jwt_identity, jwt_required
from app import app, db
from flask import Blueprint, request
from flask_restx import Resource, Api

from app.users.models import User

from datetime import datetime

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token"
    }
}

users_bp = Blueprint('user', __name__)
api = Api(users_bp,  authorizations=authorizations)


@api.route('/availability')
class SetAvailability(Resource):
    @api.doc(security='apikey')
    @api.header('Content-Type', 'application/json')
    @jwt_required()
    def post(self):
        data = request.json
        id = get_jwt_identity()
        user = User.query.filter_by(id=id).first()
        user.updateAvaiability(data['dates'])
        if user:
            return {'Status': 'OK', 'message': 'Availability set'}, 200

        return {"msg": "User not found"}, 404
