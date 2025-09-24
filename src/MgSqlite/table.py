from .sql_interraction import SQL_Execution
#from .database import Database
from .gui import TableViewer
from .json_convert import _createFile

class Table(SQL_Execution):
    """
    Initialize a new Table object and create the table in the database if it does not exist.

    Parameters
    ----------
    **kwargs : dict
        Expected keys:
            - `database` (Database): The database object this table belongs to.
            - `name` (str): The name of the table.
            - `value` (list[tuple]): A list of tuples defining the columns.
                Each tuple must follow the format:
                    (column_name: str, python_type: type, primary_key: bool, autoincrement: bool)

                - `column_name`: Name of the column.
                - `python_type`: Python type (`int`, `str`, `float`, etc.), internally mapped to SQL.
                - `primary_key`: Whether this column is the PRIMARY KEY.
                - `autoincrement`: Whether this column uses AUTOINCREMENT.

                Example:
                [
                    ("id", int, True, True),
                    ("name", str, False, False)
                ]

    Notes
    -----
    - The SQL column types are automatically inferred from Python types.
    - The table is created in the database if it does not already exist.
    - The table instance is automatically registered in `database.tableList`.

    Example
    -------
    >>> db = Database("mydb")
    >>> users = Table(
    ...     database=db,
    ...     name="users",
    ...     value=[
    ...         ("id", int, True, True),
    ...         ("name", str, False, False)
    ...     ]
    ... )
    """
    def __init__(self, **kwargs) -> None:   #database : Database, name : str, *args : tuple
        super().__init__()
        self.name = kwargs["name"]
        self.database = kwargs["database"]
        self.database.tableList.append(self)
        self.columns = [i[0] for i in kwargs["value"]]
        self.__value = self.__createColumns(kwargs["value"])
        self.simpleExecute(self.database,"CREATE TABLE IF NOT EXISTS " + self.name + " ("+self.__value+")")

    def __createColumns(self, args : tuple) -> str:               #Take a list of tuples as a parameter and return a string that contains the command to create all the columns in the table
        value = ""
        for arg in range(len(args)):
            value += args[arg][0] + " "
            value += self.checkType(args[arg][1]) + " "
            if args[arg][2]:
                value += "PRIMARY KEY "
            if args[arg][3]:
                value += "AUTOINCREMENT"
            if len(args)>1 and arg != len(args)-1:      #Just check if a comma is needed
                value += ","
        return value

    def __tokenize(self,string):
        string = string.split()
        i = 0
        conditions = []
        while i < len(string):
            temp=[]
            temp.append(string[i])
            temp.append(string[i+1])
            temp.append(string[i+2])
            if not i > len(string)-4 and string[i+3].lower() in ("or","and"):
                temp.append(string[i+3].upper())
            conditions.append(temp)
            i+=4
        return conditions

    def __build(self,conditions):
        equality = ""
        params = []
        for i in conditions:
            equality+=f"{i[0]}{i[1]}? "
            if len(i) > 3:
                equality+=i[3] + " "
            params.append(i[2])
        return equality, params

    def selectValues(self,columnsList : list, where :  str = None):
        """
        Retrieve specific columns from the table, optionally filtered by a WHERE clause.

        Parameters
        ----------
        columnsList : list
            List of column names to retrieve. Example: ["id", "name"]
        where : str, optional
            SQL-like condition string. Example: "id = 1 AND name = 'Alice'"

        Returns
        -------
        list
            List of tuples containing the requested column values.

        Example
        -------
        >>> users.selectValues(["id", "name"], "id = 1")
        [(1, "Alice")]
        """
        columnsText=""
        for column in range(len(columnsList)):                                #Create the string who contain the name of the columns you want to get
            columnsText+= columnsList[column]
            if len(columnsList)>1 and column != len(columnsList)-1:
                columnsText+=","
        equality, values = self.__build(self.__tokenize(where))

        return self.simpleExecute(self.database,"SELECT "+columnsText+" FROM "+self.name+" WHERE ("+equality+")",values)



    def selectValuesOld(self,columnsList : list, *args : dict) -> tuple:
        """
        /!\ Deprecated
        Select an list of Column where a variable of this column is equal to a chosen value
        Take the list of column and the number you want of tuple who contains : ("name Of The Column", value you want to check if is equal : can be int or float or string or anything else)

        """
        # dict = {"column":"id","value":0,"or": true, "and" : false, "sign" : "+"}

        columnsText=""
        for column in range(len(columnsList)):                                #Create the string who contain the name of the columns you want to get
            columnsText+= columnsList[column]
            if len(columnsList)>1 and column != len(columnsList)-1:
                columnsText+=","
        
        
        value=""
        value2 = []
        for arg in range(len(args)):
            value+=str(args[arg]["column"]) + str(args[arg]["sign"]) + "?"
            if len(args)> 1 and arg != len(args)-1:
                condition=str(args[arg]["condition"])
                value +=str(condition.upper())
            value2.append(args[arg]["value"])
        
        return self.simpleExecute(self.database,"SELECT "+columnsText+" FROM "+self.name+" WHERE ("+value+")",value2)

    
    def deleteTable(self) -> None:
            """
            Delete the table from the database.

            Notes
            -----
            - The table will be removed if it exists.
            - This action is irreversible.

            Example
            -------
            >>> users.deleteTable()
            """
            self.simpleExecute(self.database,"DROP TABLE IF EXISTS "  + self.name)

    def addValue(self, values : tuple, columns : list = []) -> None:
        """
        Insert or replace a row in the table.

        Parameters
        ----------
        values : tuple
            Tuple of values to insert into the table. Example: (1, "Alice")
        columns : list, optional
            List of column names corresponding to the values. If omitted, all columns are used.
            Example: ["id", "name"]

        Notes
        -----
        - This uses a REPLACE INTO query, which will insert a new row or replace an existing row
        if a PRIMARY KEY conflict occurs.

        Example
        -------
        >>> users.addValue((1, "Alice"), ["id", "name"])
        """
        questionMark = ""
        columnsText = ""
        
        for val in range(len(values)):
            #valueText+=values[val]
            questionMark+="?"
            if len(values)>1 and val != len(values)-1:                #add question mark           really i hate the fact that python use this fucking "#" for comment, why python didn't use "//"" it's a lot better, more prettyyy   but no python need to be selfish and do something that he think is original BUT NO IT'S JUST UGLY
                questionMark+=","

        if len(columns)>0:
            columnsText+=" ("
            for column in range(len(columns)):                                  #Fourth time that this part of code repeat, maybe i need to create a function for that but later
                columnsText+=columns[column]
                if len(column)>1 and column != len(columns)-1:   
                    columnsText +=","
            columnsText+") "
        
    
        self.simpleExecute(self.database,"REPLACE INTO "+self.name + columnsText+" VALUES("+questionMark+")",values)    #Compare to INSERT INGORE Or INSERT … ON DUPLICATE KEY UPDATE

    def addMultipleValues(self,values : list) -> None:
        """
        Insert or replace multiple rows in the table.

        Parameters
        ----------
        values : list of tuples
            Each tuple contains values for one row.
            Example: [(1, "Alice"), (2, "Bob")]

        Notes
        -----
        - Internally calls `addValue` for each row.
        - Uses REPLACE INTO, so existing rows with the same PRIMARY KEY will be replaced.

        Example
        -------
        >>> users.addMultipleValues([(1, "Alice"), (2, "Bob")])
        """
        for value in values:
            self.addValue(value)

    def updateValue(self,columnEqualityList : list, where : str = None):
        """
        Update rows in the table based on a SQL-like WHERE string.

        Parameters
        ----------
        columnEqualityList : list of tuples
            List of columns to update with their new values.
            Each tuple: (column_name, new_value)
            Example: [("name", "Alice")]
        where : str, optional
            SQL-like condition string to filter rows.
            Can include multiple conditions combined with AND / OR.
            Example: "id = 1 AND name = 'Ted' OR status = 'active'"

        Notes
        -----
        - Executes an UPDATE query internally.
        - Multiple columns can be updated at once.
        - Conditions are safely converted to parameterized SQLite queries.

        Example
        -------
        >>> users.updateValue([("name", "Alice")], "id = 1 AND name = 'Ted'")
        """
        columnText = ""
        value = []
        condition = ""
        for column in range(len(columnEqualityList)):
            columnText += columnEqualityList[column][0] + "=?"
            value.append(columnEqualityList[column][1])
            if len(columnEqualityList) >1 and column != len(columnEqualityList)-1:
                columnText+=","

        equality, values = self.__build(self.__tokenize(where))

        self.simpleExecute(self.database,"UPDATE "+self.name+" SET "+columnText+" WHERE "+equality,values)


    def updateValueOld(self,columnEqualityList : list, *args : tuple) -> None:
        """
        /!\ Deprecated
        """
        columnText = ""
        value = []
        condition = ""
        for column in range(len(columnEqualityList)):
            columnText += columnEqualityList[column][0] + "=?"
            value.append(columnEqualityList[column][1])
            if len(columnEqualityList) >1 and column != len(columnEqualityList)-1:
                columnText+=","

        for arg in range(len(args)):                                         
            condition+=args[arg][0] + "=?"
            value.append(args[arg][1])
            if len(args)>1 and arg != len(args)-1:
                if args[arg][2]:                           
                    condition+=" AND "
                else:
                    condition+=" OR "

        self.simpleExecute(self.database,"UPDATE "+self.name+" SET "+columnText+" WHERE "+condition,value)

    def selectAll(self) -> None:
        """
        Retrieve all rows and columns from the table.

        Returns
        -------
        list of tuples
            All rows in the table.

        Example
        -------
        >>> users.selectAll()
        [(1, "Alice"), (2, "Bob")]
        """
        return self.simpleExecute(self.database,"SELECT * FROM "+self.name)

    def deleteValue(self, where : str = None) -> None:
        """
        Delete rows from the table based on a SQL-like WHERE string.

        Parameters
        ----------
        where : str, optional
            SQL-like condition string to filter rows.
            Can include multiple conditions combined with AND / OR.
            Example: "id = 1 OR name = 'Bob'"

        Notes
        -----
        - Executes a DELETE query internally.
        - Conditions are safely converted to parameterized SQLite queries.

        Example
        -------
        >>> users.deleteValue("id = 1 AND status = 'inactive'")
        """
        equality, values = self.__build(self.__tokenize(where))
        self.simpleExecute(self.database,"DELETE FROM "+self.name+" WHERE "+equality,values)

    def deleteValueOld(self, *args) -> None:
        """
        /!\ Deprecated
        """
        condition =""
        value = []

        for arg in range(len(args)):
            condition+=args[arg][0] + "=?"
            value.append(args[arg][1])
            if len(args)>1 and arg != len(args)-1:                           
                if args[arg][2]:                           
                    condition+=" AND "
                else:
                    condition+=" OR "

        self.simpleExecute(self.database,"DELETE FROM "+self.name+" WHERE "+condition,value)

    def save(self,name : str):
        result = f"CREATE TABLE IF NOT EXISTS {name}("                                    #What the fucking fuck this function do ? I don't even know where it used of even if it used somewhere, so i let it here bruh
        dict = self.__dict__
        for key, value in dict.items():
            result += str(key) + " " + self.__checkType(value) + ","
        result = result[:-1]
        result += ")"
        self.simpleExecute(self.database,result)

    def show(self) -> None:
        """
        Display the table in a graphical viewer.

        Notes
        -----
        - Opens a GUI window using TableViewer to browse table contents.
        - No return value.

        Example
        -------
        >>> users.show()
        """
        viewer = TableViewer(self)
        viewer.mainloop()

    def _createDict(self):
        value = self.selectAll()
        columns = self.__dict__["columns"]
        dico = {self.name : []}
        if value is not None:
            for i in range(len(value)):
                temp = {}
                for j in range(len(columns)):
                    temp[columns[j]]=value[i][j]

                dico[self.name].append(temp)
        else:
            print(f"Error no data in this table : {self.name}")
        return dico
    
    def convertJson(self,name : str = "default",indentVal : int = 2)->None:
        """
        Export the table contents to a JSON file.

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
        >>> users.convertJson("users_data", indentVal=4)
        """
        _createFile(self._createDict(),name,indentVal)