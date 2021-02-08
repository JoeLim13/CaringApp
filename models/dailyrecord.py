from models.base_model import BaseModel
from models.user import User
import peewee as pw
import datetime

class DailyRecord(BaseModel):
    title = pw.DateField(formats=['%Y-%m-%d'])
    completion_rate = pw.IntegerField(default=0)
    user = pw.ForeignKeyField(User, backref="dailyrecords", on_delete="CASCADE")
    date_created = pw.DateField(default=datetime.datetime.now().date())