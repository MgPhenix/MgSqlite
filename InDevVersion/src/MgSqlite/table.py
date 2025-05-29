from .sql_interraction import SQL_Execution
from .database import Database
from .gui import TableViewer

class Table(SQL_Execution):
    def __init__(self, **kwargs) -> None:   #database : Database, name : str, *args : tuple
        super().__init__()
        self.name = kwargs["name"]
        self.database = kwargs["database"]
        self.database.tableList.append(self)
        self.columns = [i[0] for i in kwargs["value"]]
        self.__value = self.__createColumns(kwargs["value"])
        self.simpleExecute(self.database,"CREATE TABLE " + self.name + " ("+self.__value+")")

    def __createColumns(self, args : tuple) -> str:               #Take a list of tuples as a parameter and return a string that contains the command to create all the columns in the table
        value = ""
        for arg in range(len(args)):
            value += args[arg][0] + " "
            value += self.__checkType(args[arg][1]) + " "
            if args[arg][2]:
                value += "PRIMARY KEY "
            if args[arg][3]:
                value += "AUTOINCREMENT"
            if len(args)>1 and arg != len(args)-1:      #Just check if a comma is needed
                value += ","
        return value

    def __checkType(self, var : type) -> str:                  #Check all the type possible and convert python type to sqlite3 type
        if var == int:
            res = "INTEGER"
        elif var == str:
            res = "TEXT"
        elif var == float:
            res = "REAL"
        else:
            res = "NULL"
        return res

    def deleteTable(self) -> None:
        self.simpleExecute(self.database,"DROP TABLE IF EXISTS "  + self.name)

    def selectValues(self, columnsList : list, *args) -> tuple:
        """
        Select an list of Column where a variable of this column is equal to a chosen value
        Take the list of column and the number you want of tuple who contains : ("name Of The Column", value you want to check if is equal : can be int or float or string or anything else)

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

        return self.simpleExecute(self.database,"SELECT "+columnsText+" FROM "+self.name+" WHERE "+value,value2)

    def _selectValuesOR(self, columnsList : list, args : list)-> tuple:    #the function is temporary
        columnsText = ""
        value = ""
        value2 = []

        for column in range(len(columnsList)):                                
            columnsText+= columnsList[column]
            if len(columnsList)>1 and column != len(columnsList)-1:
                columnsText+=","
        
        for arg in range(len(args)):                                         
            value+=args[arg][0] + "=?"
            if len(args)>1 and arg != len(args)-1:                           
                value+=" OR "
            value2.append(args[arg][1])

        return self.simpleExecute(self.database,"SELECT "+columnsText+" FROM "+self.name+" WHERE "+value,value2)

    def addValue(self, values : tuple, columns : list = []) -> None:
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
        

        self.simpleExecute(self.database,"INSERT INTO "+self.name + columnsText+" VALUES("+questionMark+")",values)

    def updateValue(self,columnEqualityList : list, *args : tuple) -> None:
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
                condition+=" AND "

        self.simpleExecute(self.database,"UPDATE "+self.name+" SET "+columnText+" WHERE "+condition,value)

    def selectAll(self) -> None:
        return self.simpleExecute(self.database,"SELECT * FROM "+self.name)

    def show(self):
        viewer = TableViewer(self)
        viewer.mainloop()