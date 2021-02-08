from flask import Blueprint, request, jsonify, abort
from datetime import date
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

@users_api_blueprint.route("/<username>")
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
                "profileImage": user.image_path,
                "tasks": [
                    activity.task for activity in user.activities
                ],
                "completion_date": [
                    activity.completion_date for activity in user.activities
                ],
                "is_completed": [
                    activity.is_completed for activity in user.activities
                ]
                })
    else:
        return abort(404)

@users_api_blueprint.route('/<id>/edit')
@jwt_required
def edit(id):
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

@users_api_blueprint.route('/<username>/dashboard')
@jwt_required
def show_dashboard(username):
    user_id = get_jwt_identity()
    user = User.get_or_none(User.id == user_id)
    if user:
        from models.dailyrecord import DailyRecord
        dailyrecords = DailyRecord.select().where(DailyRecord.date_created <= date.today()).order_by(DailyRecord.created_at.desc())
        return jsonify({
            "username": user.username,
            "dailyrecord_title": [
                dailyrecord.title for dailyrecord in dailyrecords
            ],
            "dailyrecord_completion_rate" : [
                dailyrecord.completion_rate for dailyrecord in dailyrecords
            ]
        })
    else:
        return jsonify({"message": "No such user"}) 
    
@users_api_blueprint.route('/<id>', methods=['POST'])
@jwt_required
def update(id):
    user_id = get_jwt_identity()
    user = User.get_or_none(User.id == user_id)
    if user:
        params = request.json
        user.username = params.get("username")
        user.password = params.get("password")
        user.email = params.get("email")
        if user.save():
            return jsonify("Successfully update")
        else:
            return jsonify("Failed to update")
    else:
        return jsonify("No such user")
