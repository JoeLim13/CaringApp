from flask import Blueprint, request, jsonify, abort
from models.user import User
from models.activity import Activity
from datetime import date

schemes_api_blueprint = Blueprint('schemes_api',
                             __name__,
                             template_folder='templates')

@schemes_api_blueprint.route('/', methods=['POST'])
def create():
    current_user = User.get_or_none(User.username == 'ironrock')
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
def destroy(id):
    current_user = User.get_or_none(User.username == 'ironrock')
    if current_user:
        activity = Activity.get_by_id(id)
        if activity.delete_instance(recursive=True):
            return jsonify({"message": "Activity deleted successfully"})         
        else:
            return jsonify({"message": "Activity failed to delete"}) 
    else:
        return jsonify({"message": "No such user"})

@schemes_api_blueprint.route('/<int:id>/edit')
def edit(id):
    user = User.get_or_none(User.username == 'ironrock')
    if user:
        activity = Activity.get_or_none(Activity.id== id)
        if activity:
            return jsonify({
                "username": user.username,
                "email": user.email,
                "tasks": [
                    activity.task 
                ],
                "completion_date": [
                    activity.completion_date 
                ],
                "is_completed": [
                    activity.is_completed
                ]})
        else:
            return jsonify({"message": "No such activity"})
    else:
        return jsonify({"message": "No such user"})

@schemes_api_blueprint.route('/<int:id>/update', methods=['POST'])
def update(id):
    current_user = User.get_or_none(User.username == 'ironrock')
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
 