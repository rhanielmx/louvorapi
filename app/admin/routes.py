from app import app
from app.users.models import User
from flask import Blueprint, jsonify, request
from flask_jwt_extended import (create_access_token, get_jwt_identity,
                                jwt_required, unset_jwt_cookies)
from flask_restx import Api, Resource, fields

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
        print(request.json)
        #check if request provider is credentials, google, facebook or spotify and get the fields accordingly
        provider = request.json.get('provider', None)
        if (provider == 'credentials'):
            username = request.json['username']
            password = request.json['password']
            user = User.query.filter_by(username=username, password=password).first()
            if user:
                access_token = create_access_token(identity=user.username)
                return {'access_token': access_token}, 200
            else:
                return {'message': 'Invalid credentials'}, 401
        else:
            email = request.json.get('email', None)
            if email:
                user = User.query.filter_by(email=email).first()
                if user:                    
                    if provider not in user.providers:
                        user.providers.append(provider)
                        user.save()
                    access_token = create_access_token(identity=user.id)
                    return {'access_token': access_token}, 200
            else:
                pass
                #create user                      
            

        username = request.json.get("username", None)
        password = request.json.get("password", None)
        print(username, password)

        user = User.query.filter_by(username=username).first()
        print(user)
        if not user or user.password != password:
            return {"msg": "Wrong email or password"}, 401

        access_token = create_access_token(identity=user.id)#, additional_claims=user.json())
        response = {"token":access_token, "user":user.json()}
        return response

    
    @api.expect(token_model)
    def options(self):
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        print(username, password)

        user = User.query.filter_by(username=username).first()

        if not user or user.password != password:
            return {"msg": "Wrong email or password"}, 401

        access_token = create_access_token(identity=user.id)#, additional_claims=user.json())
        response = {"token":access_token, "user":user.json()}
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
