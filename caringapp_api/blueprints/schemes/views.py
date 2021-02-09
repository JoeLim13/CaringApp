from flask import Blueprint, request, jsonify, abort
from models.user import User
from models.activity import Activity
from datetime import date
from flask_jwt_extended import jwt_required, get_jwt_identity

schemes_api_blueprint = Blueprint('schemes_api',
                             __name__,
                             template_folder='templates')

@schemes_api_blueprint.route('/', methods=['POST'])
@jwt_required
def create():
    user_id = get_jwt_identity()
    current_user = User.get_or_none(User.id == user_id)
    if current_user: 
        params = request.json
        new_activity = Activity(task=params.get('activity'),
                    completion_date=params.get('date'),
                    user = current_user.id)
        if new_activity.save():
            return jsonify({"message": "Activity added successfully"})      
        else:
            return jsonify({"message": "Activity failed to add"}) 
    else:
        return jsonify({"message": "No such user"})

@schemes_api_blueprint.route('/<int:id>/delete', methods=['POST'])
@jwt_required
def destroy(id):
    user_id = get_jwt_identity()
    current_user = User.get_or_none(User.id == user_id)
    if current_user:
        activity = Activity.get_by_id(id)
        if activity.delete_instance(recursive=True):
            return jsonify({"message": "Activity deleted successfully"})         
        else:
            return jsonify({"message": "Activity failed to delete"}) 
    else:
        return jsonify({"message": "No such user"})

@schemes_api_blueprint.route('/<int:id>/edit')
@jwt_required
def edit(id):
    user_id = get_jwt_identity()
    current_user = User.get_or_none(User.id == user_id)
    if current_user:
        activity = Activity.get_or_none(Activity.id== id)
        if activity:
            return jsonify({
                "user_id": current_user.id,
                "username": current_user.username,
                "email": current_user.email,
                "activity_id": activity.id,
                "task": activity.task,
                "completion_date": activity.completion_date,
                "is_completed": activity.is_completed
                })
        else:
            return jsonify({"message": "No such activity"})
    else:
        return jsonify({"message": "No such user"})

@schemes_api_blueprint.route('/<int:id>/update', methods=['POST'])
@jwt_required
def update(id):
    user_id = get_jwt_identity()
    current_user = User.get_or_none(User.id == user_id)
    if current_user:
        activity = Activity.get_or_none(Activity.id== id)
        if activity:
                params = request.json

                activity.is_completed = True if params.get("completed") == "on" else False

                activity.task = params.get("activity")
                activity.completion_date = params.get("date")
                
                if activity.save():
                    return jsonify({"message": "Activity updated successfully"})
                else:
                    return jsonify({"message": "Activity failed to update"})
        else:
            return jsonify({"message": "No such activity"})
    else:
        return jsonify({"message": "No such user"})
 