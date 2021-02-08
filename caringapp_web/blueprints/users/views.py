from app import scheduler
import peewee as pw
from datetime import date, time
import datetime
from models.user import User
from models.activity import Activity
from werkzeug import secure_filename
from caringapp_web.util.helpers import upload_file_to_s3
from flask_login import login_required, login_user, current_user
from flask import Blueprint, render_template, request, redirect, url_for, flash


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods = ['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    params = request.form

    new_user = User(username = params.get("username"), email = params.get("email"), password = params.get("password"))

    if new_user.save():
        flash("Successfully Signed Up")
        login_user(new_user)
        return redirect(url_for("users.show", username = new_user.username))
    else:
        for err in new_user.errors:
            flash(err, "danger")
        return redirect(url_for("users.new"))


@users_blueprint.route('/<username>', methods = ["GET"])
@login_required
def show(username):
    user = User.get_or_none(User.username == username)
    if user:
        user = pw.prefetch(user)
        return render_template("users/show.html", user = user)
    else:
        flash(f"No {username} user found", "danger")
        return redirect(url_for('home'))


@users_blueprint.route('/', methods = ["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods = ['GET'])
@login_required
def edit(id):
    user = User.get_or_none(User.id == id)
    if user:
        if current_user.id == int(id):
            return render_template("users/edit.html", user = user)
        else:
            flash("Cannot edit someone else's profile")
            return redirect(url_for('users.show', username = user.username))
    else:
        flash("No user found")
        return redirect(url_for("home"))

@users_blueprint.route('/<username>/dashboard', methods=["GET"])
@login_required
def show_dashboard(username):
    user = User.get_or_none(User.username == username)
    if user:
        from models.dailyrecord import DailyRecord
        x = datetime.datetime.now()
        print(type(x))
        y = x.strftime('%Y-%m-%d')
        print(type(y))
        a = datetime.datetime.strptime(y,"%Y-%m-%d")
        print(type(a))
        z = date.today()
        print(type(z))
        b = x.date()
        print(type(b))
        if y == z:
            print("ok")
        else:
            print("nope")
        dailyrecords = DailyRecord.select().where(DailyRecord.date_created <= date.today()).order_by(DailyRecord.created_at.desc())
        for dailyrecord in dailyrecords:
            return render_template("users/dashboard.html", user=user, dailyrecords = dailyrecords)
    else:
        flash("No User Found")
        return redirect(url_for('home'))

@users_blueprint.route('/<id>', methods = ['POST'])
@login_required
def update(id):
    user = User.get_or_none(User.id == id)
    if user:
        if current_user.id == int(id):
            params = request.form
        
            user.username = params.get("username")
            user.email = params.get("email")
            password = params.get("password")

            if len(password) > 0:
                user.password = password

            if user.save():
                flash("Successfully updated details.")
                return redirect(url_for("users.show", username = user.username))
            else:
                flash("Failed to edit your profile. Try again")
                for err in user.errors:
                    flash(err)
                return redirect(url_for("users.edit", id = user.id))
        else:
            flash("You cannot edit details of another user")
            return redirect(url_for("users.show", username = user.username))
    else:
        flash("No such user!")
        redirect(url_for("home"))

@users_blueprint.route('/<id>/upload', methods=['POST'])
@login_required
def upload(id):
    user = User.get_or_none(User.id == id)
    if user:
        if current_user.id == int(id):
           
            if "profile_image" not in request.files:
                flash("No file provided!")
                return redirect(url_for("users.edit", id=id))

            file = request.files["profile_image"]

            file.filename = secure_filename(file.filename)
            
            image_path = upload_file_to_s3(file,user.username )
            
            user.image_path = image_path

            print(user.image_path)
            if user.save():
                return redirect(url_for("users.show", username=user.username))
            else:
                flash("Could not upload image. Please try again")
                return redirect(url_for("users.edit", id=id))       
        else:
            flash("Cannot edit users other than yourself!")
            return redirect(url_for("users.show", username=user.username))
    else:
        flash("No such user!")
        redirect(url_for("home"))

@scheduler.task('cron', id='do_save_to_dashboard', hour='18', minute='30', second='0')
def save_to_dashboard():
    user = User.get_or_none(User.username == username)
    if user:
        current_day = date.today()
        previous_day = Activity.select().where((Activity.completion_date < current_day)).order_by(Activity.completion_date.desc()).limit(1)
        for p in previous_day:
            print(p.completion_date)
        yesterday = p.completion_date
        if yesterday:
            from models.dailyrecord import DailyRecord
            is_completed = Activity.select().where(Activity.is_completed == 1, Activity.completion_date == yesterday).count()
            print(is_completed)
            task = Activity.select().where(Activity.completion_date == yesterday).count()
            print(task)
            completion_rate = is_completed / task * 100
            title = yesterday
            relationship = DailyRecord(title = title, completion_rate = completion_rate, user = user.id)
            if relationship.save() :
                print('Successfully saved')
            else :
                print('Something wrong in the code')
        else:
            print('Query Problem')
    else:
        print('No such user')  