from models.base_model import BaseModel
from models.user import User
import peewee as pw
from datetime import date, time
import datetime


class Activity(BaseModel):
    task = pw.CharField(null=False)
    completion_date = pw.DateField(formats=['%Y-%m-%d'])
    is_completed = pw.BooleanField(default=False)
    user = pw.ForeignKeyField(User, backref="activities", on_delete="CASCADE")
    
    
    
    def validate(self):
        #Completion Date cannot be earlier than current day
        current_day = date.today()
        key_in_date = datetime.datetime.strptime(self.completion_date, "%Y-%m-%d").date()
        previous_day = Activity.select(Activity.completion_date).where(key_in_date < current_day)
        if previous_day:
            self.errors.append('Cannot enter previous day')
    
            
            
        

        
        
        
