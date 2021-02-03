from flask import Blueprint, render_template, flash, redirect, url_for, request
from models.activity import Activity
from models.user import User

schemes_blueprint = Blueprint('schemes',
                            __name__,
                            template_folder='templates')

@schemes_blueprint.route('/new', methods=['GET'])
def new():
    print("HELLO")
    return render_template('schemes/new.html')

@schemes_blueprint.route('/', methods=['POST'])
def create():
    print("HELLO")
    current_user = User.get_or_none(User.username == 'ironrock')
    if current_user:
        new_activity = Activity(task=request.form['activity'],
                    completion_date=request.form['date'],
                    user = current_user.id)
        if new_activity.save():
            flash("Activity has been succesfully added!")
            return redirect(url_for('users.show', username = current_user.username))
        else:
            flash("Not added!")
            return render_template('schemes/new.html', completion_date=request.form['date'], errors=new_activity.errors)
    else:
        flash("No such user")
        return redirect(url_for('home'))

@schemes_blueprint.route('/<int:id>/delete', methods=['POST'])
def destroy(id):
    current_user = User.get_or_none(User.username == 'ironrock')
    if current_user:
        activity = Activity.get_by_id(id)
        if activity.delete_instance(recursive=True):
            flash("Successfully deleted activity!")
            return redirect(url_for('users.show', username = current_user.username))
        else:
            flash("Unable to delete activity!")
            return redirect(url_for('users.show', username = current_user.username))
    else:
        flash("No such user")
        return redirect(url_for('home'))

@schemes_blueprint.route('/<int:id>/edit', methods=['GET'])
def edit(id):
    current_user = User.get_or_none(User.username == 'ironrock')
    if current_user:
        activity = Activity.get_or_none(Activity.id== id)
        if activity:
            if activity.id == int(id):
                return render_template("schemes/edit.html", activity = activity)
            else:
                flash("Cannot edit!")
                return redirect(url_for("users.show", username=current_user.username))
        else:
            flash("No such activity")
            return redirect(url_for("users.show", username=current_user.username))
    else:
        flash("No such user!")
        return redirect(url_for("home"))

@schemes_blueprint.route('/<int:id>/update', methods=['POST'])
def update(id):
    current_user = User.get_or_none(User.username == 'ironrock')
    if current_user:
        activity = Activity.get_or_none(Activity.id== id)
        if activity:
            if activity.id == int(id):
                params = request.form

                activity.is_completed = True if params.get("completed") == "on" else False

                activity.task = params.get("activity")
                activity.completion_date = params.get("date")
                
                if activity.save():
                    flash("Successfully updated Activity!")
                    return redirect(url_for("users.show", username=current_user.username))
                else:
                    flash("Unable to edit!")
                    return redirect(url_for("schemes.edit", id=activity.id))
            else:
                flash("Cannot edit more than one activity!")
                return redirect(url_for("users.show", username=current_user.username))
        else:
            flash("No such activity!")
            return redirect(url_for("users.show", username=current_user.username))
    else:
        flash("No such user!")
        redirect(url_for("home"))
        
