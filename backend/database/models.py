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
    active_loans = IntegerField()

    class Meta:
        database = database
        table_name = "users"

class Book (Model):
    title = CharField()
    description = TextField()
    total_stock = IntegerField()
    available_stock = IntegerField()

    class Meta:
        database = database
        table_name = "books"

class Loan (Model):
    user = ForeignKeyField(User,backref="loans")
    book = ForeignKeyField(Book, backref="loans")
    lend_date = DateTimeField(default=datetime.now)
    return_date = DateTimeField()
    expected_return_date = DateTimeField()
    penalty = IntegerField()
    is_active = BooleanField()

    class Meta:
        database = database
        table_name = "loans"

class Author(Model):
    name = CharField()
    description = TextField()
    nationality = CharField()

    class Meta:
        database = database
        table_name = "authors"

class BookAuthor(Model):
    book = ForeignKeyField(Book,backref="authors")
    author = ForeignKeyField(Author,backref="books")

    class Meta:
        database = database
        table_name = "books_authors"

