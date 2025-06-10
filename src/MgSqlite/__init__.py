
"""
MgSqlite is a Python module designed to create and interact with SQLite databases without writing raw SQL. It leverages sqlite3 under the hood, allowing you to manage your database effortlessly using simple function calls.
"""

__version__ = "0.6"

from .database import Database
from .sql_interraction import SQL_Execution
from .table import Table
