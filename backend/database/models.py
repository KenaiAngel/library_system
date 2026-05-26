from peewee import *
from datetime import datetime

database = MySQLDatabase(
    "Library_FinalProject",
    user="root",
    password="sapo123",
    host="localhost",
    port=3306,
)

class User(Model):
    email = CharField(max_length=80, unique=True)
    username = CharField(max_length=50)
    password = CharField()
    role = CharField()

    class Meta:
        database = database
        table_name = "users"
