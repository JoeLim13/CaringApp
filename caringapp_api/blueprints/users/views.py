from flask import Blueprint, request, jsonify, abort
from datetime import date
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug import secure_filename
from caringapp_web.util.helpers import upload_file_to_s3, s3
from models.user import User
from app import app


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
        from models.activity import Activity
        activities = Activity.select().where(Activity.user == user.id)
        if activities:
            return jsonify({
                    "user_id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "profileImage": app.config.get("S3_LOCATION") + user.image_path,
                    "activity": [{
                        "activity_id": activity.id,
                        "tasks": activity.task,
                        "completion_date": activity.completion_date,
                        "is_completed": activity.is_completed                       
                    } for activity in activities]})
        else:
            return jsonify({"messages" : "User does not have any activities yet"})
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
            "profileImage": app.config.get("S3_LOCATION") + user.image_path
            }
        )
    else:
        return jsonify({"messages": "No such user"})

@users_api_blueprint.route('/<username>/dashboard')
@jwt_required
def show_dashboard(username):
    user_id = get_jwt_identity()
    user = User.get_or_none(User.id == user_id)
    if user:
        from models.dailyrecord import DailyRecord
        dailyrecords = DailyRecord.select().where(DailyRecord.date_created <= date.today()).order_by(DailyRecord.created_at.desc())
        if dailyrecords:
            return jsonify({
                "user_id": user.id,
                "username": user.username,
                "dailyrecord": [{
                    "dailyrecord_id": dailyrecord.id,
                    "dailyrecord_title": dailyrecord.title,
                    "dailyrecord_completion_rate" : dailyrecord.completion_rate                     
                } for dailyrecord in dailyrecords]})
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
            return jsonify({"message": "Successfully update"})
        else:
            return jsonify({"message": "Failed to update"})
    else:
        return jsonify({"message": "No such user"})

@users_api_blueprint.route('/image', methods=['POST'])
@jwt_required
def upload_image():
    user_id = get_jwt_identity()
    user = User.get_or_none(User.id == user_id)
    if user:          
        if "profile_image" not in request.files:
            return jsonify({"messages" : "No profile_image key in request.files"})
        
        file = request.files["profile_image"]
        
        if file.filename == "":
            return jsonify({"messages" : "Please select a file"})
        
        if file:
            file.filename = secure_filename(file.filename)
                
            image_path = upload_file_to_s3(file,user.username )
                
            user.image_path = image_path

            if user.save():
                return jsonify({"messages" : "Uploaded successfully", "profileImage" : app.config.get("S3_LOCATION") + user.image_path}) 
            else:
                return jsonify({"messages" : "Error occured during uploading"})  
        else: 
            return jsonify({"messages" : "No file selected"})
    else:
        return jsonify({"messages" : "No such user"})
