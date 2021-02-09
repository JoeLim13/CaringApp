from flask_apscheduler import APScheduler
from app import app
import peewee as pw
from datetime import date, time
import datetime
from models.user import User
from models.activity import Activity

scheduler = APScheduler()

# @scheduler.task('interval', id='do_job_1', seconds=5, misfire_grace_time=900)
# def job1():
#     print('Job 1 executed')

@scheduler.task('cron', id='do_backgroundjob', hour='16', minute='29', second='0')
def backgroundjob():
    all_user = User.select()
    for user in all_user:
        print(user.username)
        if user:
            current_day = date.today()
            previous_day = Activity.select().where((Activity.completion_date < current_day)).order_by(Activity.completion_date.desc()).limit(1)
            for p in previous_day:
                print(p.completion_date)
            yesterday = p.completion_date
            if yesterday:
                from models.dailyrecord import DailyRecord
                is_completed = Activity.select().where(Activity.is_completed == 1, Activity.completion_date == yesterday, Activity.user == user.id).count()
                print(is_completed)
                task = Activity.select().where(Activity.completion_date == yesterday, Activity.user == user.id).count()
                if task == 0:
                    print(user.id)
                    print(task)
                    completion_rate = 0
                    title = yesterday
                    relationship = DailyRecord(title = title, completion_rate = completion_rate, user = user.id)
                else:
                    print(user.id)
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
    print("done")

scheduler.init_app(app)
scheduler.start()


