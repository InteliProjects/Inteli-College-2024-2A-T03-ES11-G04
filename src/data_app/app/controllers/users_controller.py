from flask import Blueprint, request, jsonify
from services.user_service import get_all_users, get_user_by_id, update_user, delete_user
from flask_jwt_extended import jwt_required

user_blueprint = Blueprint('users', __name__)

@user_blueprint.route('/get_all', methods=['GET'])
def get_users():
    users = get_all_users()
    return jsonify([{"id": user.id, "username": user.username, "user_type": user.user_type, "store": user.store} for user in users])

@user_blueprint.route('/get/<int:id>', methods=['GET'])
def get_user(id):
    user = get_user_by_id(id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"id": user.id, "username": user.username, "user_type": user.user_type, "store": user.store})

@user_blueprint.route('/update/<int:id>', methods=['PUT'])
def update_user(id):
    user = get_user_by_id(id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    update_user(user, data)

    return jsonify({"message": "User updated"}), 200

@user_blueprint.route('/delete/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = get_user_by_id(id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    delete_user(user)
    return jsonify({"message": "User deleted"}), 200
