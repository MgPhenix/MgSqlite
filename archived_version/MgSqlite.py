import sqlite3
import os


class SQL_Execution:

    def simpleExecute(self,database : object, command : str, list : list = []) -> tuple:                  #Function for execute One command in sqlite3, just to shorten the code
        """
        Execute sql script, return a value if the command is a selection return None if not
        """
        try:
            conn = sqlite3.connect(database.databaseName)
        except:
            print("Error : can't connect to the database")

        cur = conn.cursor()
        try:
            print(command)                                                                        
            res = cur.execute(command,list)                                                             # I doesn't like this line because it just repeat the same line 2 time, but it's necessary because when you don't do a SELECT for getting a result you don't have a list to put as parameter      edit : Nevermind i found how to fix that
        except:
            print("Error : can't execute command")

        res = res.fetchall()
        conn.commit()
        conn.close()
        if len(res)>=1:
            return res[0]








class Database(SQL_Execution):
    def __init__(self, name : str):
        super().__init__()                        
        self.databaseName = str(name)+".db"                               
        try:
            conn = sqlite3.connect(self.databaseName)
            conn.close()
        except:
            print("Error : Incorrect Name")

    def simpleExecute(self, command : str, list : list = []) -> tuple:                  #Function for execute One command in sqlite3, just to shorten the code
        """
        Execute sql script, return a value if the command is a selection return None if not
        """
        try:
            conn = sqlite3.connect(self.databaseName)
        except:
            print("Error : can't connect to the database")

        cur = conn.cursor()
        try:                                                                        
            res = cur.execute(command,list)                                                             # I doesn't like this line because it just repeat the same line 2 time, but it's necessary because when you don't do a SELECT for getting a result you don't have a list to put as parameter      edit : Nevermind i found how to fix that
        except:
            print("Error : can't execute command")

        res = res.fetchall()
        conn.commit()
        conn.close()
        if len(res)>=1:
            return res[0]

    def checkType(self, var : type) -> str:                  #Check all the type possible and convert python type to sqlite3 type
        if var == int:
            res = "INTEGER"
        elif var == str:
            res = "TEXT"
        elif var == float:
            res = "REAL"
        else:
            res = "NULL"
        return res

    def createColumns(self, args : tuple) -> str:               #Take a list of tuples as a parameter and return a string that contains the command to create all the columns in the table
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

    def createTable(self, name : str, *args : tuple) -> None:       #Create a table with all the argument provided                                                                                             # the prototype is under the particul accelerator
        """
        Create a Table in the Database, 
        Argument:
            name : str,
            *args : Tuple -> (nameOfTable : str, 
                              type : type,   
                              if Primary Key : Bool, 
                              if Autoincrement : Bool  
                              )
        """
        value = self.createColumns(args)                                         #value contains all the columns that will be in the table
        self.simpleExecute("CREATE TABLE " + name + " ("+value+")")

    def dropIfTableExist(self, name : str) -> None:
        self.simpleExecute("DROP TABLE IF EXIST " + name)

    def selectFromTable(self, nameTable : str, columnsList : list, *args) -> tuple:
        """
        Select an list of Column where a variable of this column is equal to a chosen value
        Take the name of table, the list of column and the number you want of tuple who contains : ("name Of The Column", value you want to check if is equal : can be int or float or string or anything else)

        """
        columnsText = ""
        value = ""
        value2 = []

        for column in range(len(columnsList)):                                #Create the string who contain the name of the columns you want to get
            columnsText+= columnsList[column]
            if len(columnsList)>1 and column != len(columnsList)-1:
                columnsText+=","
        
        for arg in range(len(args)):                                         #Create the string who contain the variable to check 
            value+=args[arg][0] + "=?"
            if len(args)>1 and arg != len(args)-1:                           #Check if is needed to put an "AND" when you have multiple variable to check
                value+=" AND "
            value2.append(args[arg][1])

        return self.simpleExecute("SELECT "+columnsText+" FROM "+nameTable+" WHERE "+value,value2)

    def addValToTable(self, nameTable : str, values : tuple, columns : list = []) -> None:
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
        

        self.simpleExecute("INSERT INTO "+nameTable + columnsText+" VALUES("+questionMark+")",values)

    def deleteDatabase(self):
        os.remove(self.databaseName)


class Table(SQL_Execution):
    def __init__(self, database : object, name : str, *args : tuple):
        super().__init__()
        self.name = name
        self.database = database
        self.value = self.createColumns(args)
        print("CREATE TABLE " + self.name + " ("+self.value+")")
        print(self.database.databaseName)
        self.simpleExecute(self.database,"CREATE TABLE " + self.name + " ("+self.value+")")

    def createColumns(self, args : tuple) -> str:               #Take a list of tuples as a parameter and return a string that contains the command to create all the columns in the table
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

    def checkType(self, var : type) -> str:                  #Check all the type possible and convert python type to sqlite3 type
        if var == int:
            res = "INTEGER"
        elif var == str:
            res = "TEXT"
        elif var == float:
            res = "REAL"
        else:
            res = "NULL"
        return res



if __name__ == "__main__":
    os.remove("data.db")
    data = Database("data")
    table1 = Table(data, 
                   "table1", 
                   ("id",int,True,True),
                   ("name",str,False,False))
    
    data.selectFromTable("table1",["id","name"],("id",0))