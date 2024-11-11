from flask import Blueprint, request, jsonify
from services.user_service import create_user, get_user_by_username, get_user_by_id
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user_type = data.get('user_type')
    store = data.get('store')

    response, status_code = create_user(username, password, user_type, store)
    return jsonify(response), status_code

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = get_user_by_username(username)
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token}), 200

@auth_blueprint.route('/me', methods=['GET'])
@jwt_required()
def get_me():
    user_id = get_jwt_identity()
    user = get_user_by_id(user_id)
    return jsonify({"username": user.username, "user_type": user.user_type, "store": user.store}), 200
