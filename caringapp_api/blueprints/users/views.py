from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.user import User


users_api_blueprint = Blueprint('users_api',
                                 __name__,
                                 template_folder='templates')


@users_api_blueprint.route('/', methods=['POST'])
def create():
    params = request.json
    new_user = User(username = params.get("username"), email = params.get("email"), password = params.get("password"))
    if new_user.save():
        token = create_access_token(identity = new_user.id)
        return jsonify({"token": token})
    else:
        return jsonify([err for err in new_user.errors])

@users_api_blueprint.route("/<username>", methods=['GET'])
@jwt_required
def show(username):
    user_id = get_jwt_identity()
    user = User.get_or_none(User.id == user_id)
    if user:
        return jsonify(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "profileImage": user.image_path
            }
        )
    else:
        return abort(404)

@users_api_blueprint.route('/<id>/edit', methods = ['GET'])
@jwt_required
def edit(id):
    user_id = get_jwt_identity()
    user = User.get_or_none(User.id == id)
    if user:

        return jsonify(
            {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "profileImage": user.image_path
            }
        )
    else:
        return abort(404)


@users_api_blueprint.route('/<id>', methods=['POST'])
def update(id):
    user = User.get_or_none(User.id == id)
    params = request.json
    edit_user = User(username = params.get("username"), email = params.get("email"), password = params.get("password"))
    if edit_user.save():
        return jsonify("Successfully update")
    else:
        return jsonify("Failed to update")