from peewee import *
from playhouse.migrate import *
from datetime import datetime
from models import database as connection

migrator = MySQLMigrator(connection)

active_loans = IntegerField(null=True)

migrate(
    migrator.add_column(
        'users',      # nombre tabla
        'active_loans',     # nombre columna
        active_loans
    )
)