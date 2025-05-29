
"""
MgSqlite is module for create and interract with database without using sql, the module use sqlite3 but for create and interract with database you don't need to code in sql just use all the functions
"""

__version__ = "0.5"

from .database import Database
from .sql_interraction import SQL_Execution
from .table import Table
