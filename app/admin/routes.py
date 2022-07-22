from app import app
from flask import Blueprint, request, jsonify
from flask_restx import Resource, Api, fields
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, unset_jwt_cookies
from app.users.models import User

admin_bp = Blueprint('admin',__name__)
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token"
    }
}

api = Api(admin_bp, authorizations=authorizations)

token_model = api.model('Token',{
    'username': fields.String,
    'password': fields.String
})


@api.route('/token', methods=['POST'])
class Token(Resource):
    @api.expect(token_model)
    def post(self):
        username = request.json.get("username", None)
        password = request.json.get("password", None)

        user = User.query.filter_by(username=username).first()

        if not user or user.password != password:
            return {"msg": "Wrong email or password"}, 401

        access_token = create_access_token(identity=user.id)#, additional_claims=user.json())
        response = {"token":access_token, "user":user.json()}
        return response

    
    @api.expect(token_model)
    def options(self):
        username = request.json.get("username", None)
        password = request.json.get("password", None)

        user = User.query.filter_by(username=username).first()

        if not user or user.password != password:
            return {"msg": "Wrong email or password"}, 401

        access_token = create_access_token(identity=user.id)
        response = {"access_token":access_token, "user":user.json()}
        return response

@api.route("/logout", methods=["POST"])
class Logout(Resource):
    def post(self):
        response = jsonify({"msg": "logout successful"})
        unset_jwt_cookies(response)
        return response

@api.route('/user')
class GetUser(Resource):
    @api.doc(security='apikey')
    @jwt_required()
    def get(self):
        id = get_jwt_identity()
        user = User.query.filter_by(id=id).first()
        if user:
            return user.json()
        return {"msg": "User not found"}, 404