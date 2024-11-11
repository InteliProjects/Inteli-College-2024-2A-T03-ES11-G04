from models.user_model import User, db
from werkzeug.security import generate_password_hash

def create_user(username, password, user_type, store):
    if User.query.filter_by(username=username).first():
        return {"error": "User already exists"}, 400

    user = User(username=username, user_type=user_type, store=store)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return {"message": "User registered successfully"}, 201

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_all_users():
    return User.query.all()

def get_user_by_id(user_id):
    return User.query.get(user_id)

def update_user(user, data):
    user.username = data.get('username', user.username)
    user.user_type = data.get('user_type', user.user_type)
    user.store = data.get('store', user.store)
    db.session.commit()

def delete_user(user):
    db.session.delete(user)
    db.session.commit()
