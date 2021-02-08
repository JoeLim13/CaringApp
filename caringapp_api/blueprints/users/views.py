from flask import Blueprint, request, jsonify, abort
from models.user import User
from datetime import date

users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

@users_api_blueprint.route('/<username>')
def show(username):
    user = User.get_or_none(User.username == username)
    if user:
        return jsonify({
            "username": user.username,
            "email": user.email,
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
        return jsonify({"message": "No such user"}) 

@users_api_blueprint.route('/<username>/dashboard')
def show_dashboard(username):
    user = User.get_or_none(User.username == username)
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
    