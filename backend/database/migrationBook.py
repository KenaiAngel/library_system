from playhouse.migrate import *
from models import database as connection

migrator = MySQLMigrator(connection)

is_active = BooleanField(default=True)

migrate(
    migrator.add_column(
        'books',
        'is_active',
        is_active
    )
)