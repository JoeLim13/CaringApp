from flask import Blueprint, render_template, flash, redirect, url_for, request
from models.user import User
from models.activity import Activity
from datetime import date, time
import datetime
from peewee import fn
from app import scheduler

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')

@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    user = User.get_or_none(User.username == username)
    if user:
        return render_template("users/show.html", user=user)
    else:
        flash("No User Found")
        return redirect(url_for('home'))


@users_blueprint.route('/<username>/dashboard', methods=["GET"])
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

@scheduler.task('cron', id='do_save_to_dashboard', hour='0', minute='0', second='0')
def save_to_dashboard():
    user = User.get_or_none(User.username == 'ironrock')
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
