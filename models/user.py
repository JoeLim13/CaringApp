from models.base_model import BaseModel
import peewee as pw


class User(BaseModel):
    username = pw.CharField(unique=True, null=False) 
    password = pw.TextField(null=False)
    email = pw.CharField(null=False)
