from persistence.postgre_db_context import PostgreDbContext
from persistence.sqlite_db_context import SqliteDbContext
from settings import DB_ENGINE

match DB_ENGINE:
    case "sqlite":
        context = SqliteDbContext()
        connection_string = context.get_connection_string()
        db_context = context.get_db_context
    case "postgresql":
        context = PostgreDbContext()
        connection_string = context.get_connection_string()
        db_context = context.get_db_context
    case __:
        context = SqliteDbContext()
        connection_string = context.get_connection_string()
        db_context = context.get_db_context
