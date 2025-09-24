import os
from .sql_interraction import SQL_Execution
from .json_convert import _createFile,_loadFile
from .table import Table

class Database(SQL_Execution):
    """
    Initialize a new Database object and connect to a SQLite database file.

    Parameters
    ----------
    name : str, optional
        The name of the database (without extension). Default is "default".
        The actual file used will be `name + ".db"`.

    Attributes
    ----------
    databaseName : str
        The full filename of the SQLite database.
    tableList : list
        List of Table instances created in this database.
    printSQL : bool
        If True, executed SQL statements will be printed for debugging.
    _tryConnect : method
        Internal method used to attempt connection to the SQLite database.

    Notes
    -----
    - If the database file does not exist, it will be created automatically.
    - Tables created in this database should be registered in `tableList`.

    Example
    -------
    >>> db = Database("mydb")
    >>> print(db.databaseName)
    "mydb.db"
    """
    def __init__(self,name : str = "default") -> None:
        super().__init__()                        
        self.databaseName = str(name)+".db"
        self.tableList = []
        self.printSQL = False                               
        self._tryConnect(self.databaseName)
        
    def turnOffPrintSQL(self) -> None:
        """
        Disable printing of executed SQL commands.

        Notes
        -----
        - Useful to prevent debug output when running multiple commands.

        Example
        -------
        >>> db.turnOffPrintSQL()
        """
        self.printSQL = False

    def turnOnPrintSQL(self) -> None:
        """
        Enable printing of executed SQL commands.

        Notes
        -----
        - Useful for debugging to see SQL queries and parameters.

        Example
        -------
        >>> db.turnOnPrintSQL()
        """
        self.printSQL = True

    def deleteAllTable(self) -> None:
        """
        Delete all tables registered in this database.

        Notes
        -----
        - Calls `deleteTable()` for each table in `tableList`.
        - Errors are caught if a table cannot be deleted.

        Example
        -------
        >>> db.deleteAllTable()
        """
        try:
            for table in self.tableList:
                table.deleteTable()
        except:
            print("Can't delete table or table does not exist")    
            
    def deleteDatabase(self) -> None:
        """
        Delete the database file from disk.

        Notes
        -----
        - Removes the file `databaseName`.
        - Use with caution: this is irreversible.

        Example
        -------
        >>> db.deleteDatabase()
        """
        try:
            os.remove(self.databaseName)
        except :
            print("Can't delete database")

    def _generateDict(self):
        name = self.databaseName.replace(".db","")
        dico = {name : []}
        for table in self.tableList:
            dico[name].append(table._createDict())
        return dico

    def convertJson(self,name : str = "default",indentVal : int = 2):
        """
        Export the entire database to a JSON file.

        Parameters
        ----------
        name : str, optional
            Name of the output JSON file (without extension). Default is "default".
        indentVal : int, optional
            Number of spaces for indentation in the JSON file. Default is 2.

        Notes
        -----
        - The JSON file will be saved as `name + ".json"`.

        Example
        -------
        >>> db.convertJson("my_database", indentVal=4)
        """
        _createFile(self._generateDict(),name,indentVal)

    def AddTableFromJson(self,file : str) -> Table:
        """
        Create a table in the database from a JSON file.

        Parameters
        ----------
        file : str
            Path to the JSON file containing table data.

        Returns
        -------
        Table
            The Table instance created and populated from the JSON file.

        Notes
        -----
        - Column types are inferred from the JSON values.
        - All rows in the JSON file are inserted into the table.

        Example
        -------
        >>> users_table = db.AddTableFromJson("users.json")
        """
        dict = _loadFile(file)
        name = [key for key, value in dict.items()][0]
        element = [elem for elem,val in dict[name][0].items()]
        valueList = []
        for column in element:
            valType = type(dict[name][0][column])
            valueList.append((column,valType,False,False))
        table = Table(name=name,database=self,value=valueList)
        
        allValue = []
        for dico in dict[name]:
            toAddValueList = []
            for elemt in element:
                toAddValueList.append(dico[elemt])
            allValue.append(toAddValueList)
        table.addMultipleValues(allValue)
        return table