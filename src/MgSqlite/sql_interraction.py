import sqlite3

class SQL_Execution:
    """
    Base class providing methods to execute SQL queries.

    Notes
    -----
    - Not meant to be used directly.
    - Inherited by classes like `Table` and `Database`.
    - Provides helper methods for executing, fetching, and managing SQL statements.
    """

    def simpleExecute(self,database : object, command : str, list : list = []) -> tuple:                  #Function for execute One command in sqlite3, just to shorten the code
        """
        Execute a single SQL command on the specified database.

        Parameters
        ----------
        database : object
            Database instance to execute the command on.
        command : str
            SQL command to execute.
        list : list, optional
            Optional list of parameters for parameterized queries. Default is [].

        Returns
        -------
        tuple
            Fetched results for SELECT queries.
            Returns None for commands that do not return rows (INSERT, UPDATE, DELETE).

        Notes
        -----
        - Prints the command and parameters if `database.printSQL` is True.
        - Commits changes and closes the connection automatically.

        Example
        -------
        >>> db.simpleExecute(db, "SELECT * FROM users WHERE id=?", [1])
        ((1, "Alice"),)
        """
        try:
            conn = sqlite3.connect(database.databaseName)
        except:
            print("Error : can't connect to the database")

        cur = conn.cursor()
        
        if database.printSQL:
            print(command,list)
        try:
            res = cur.execute(command,list)                                                             # I doesn't like this line because it just repeat the same line 2 time, but it's necessary because when you don't do a SELECT for getting a result you don't have a list to put as parameter      edit : Nevermind i found how to fix that
        except:
            print("Error : can't execute command")
        try:
            res = res.fetchall()
            conn.commit()
            conn.close()
            if len(res)>=1:
                return res
        except:
            print("Error : Some values seem to be mising")

    def _tryConnect(self,databaseName : str) -> None:
        """
        Try to connect to the database
        """
        try:
            conn = sqlite3.connect(databaseName)
            conn.close()
        except:
            print("Error : Incorrect Name")

    def checkType(self, var : type) -> str:                  #Check all the type possible and convert python type to sqlite3 type
        """
        Convert python type to sqlite3 type
        """
        if var == int:
            res = "INTEGER"
        elif var == str:
            res = "TEXT"
        elif var == float:
            res = "REAL"
        else:
            res = "NULL"
        return res
