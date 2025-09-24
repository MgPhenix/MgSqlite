import os
from .sql_interraction import SQL_Execution
from .json_convert import _createFile,_loadFile
from .table import Table

class Database(SQL_Execution):
    def __init__(self,name : str = "default") -> None:
        super().__init__()                        
        self.databaseName = str(name)+".db"
        self.tableList = []
        self.printSQL = False                               
        self._tryConnect(self.databaseName)
        
    def turnOffPrintSQL(self) -> None:
        self.printSQL = False

    def turnOnPrintSQL(self) -> None:
        self.printSQL = True

    def deleteAllTable(self) -> None:
        try:
            for table in self.tableList:
                table.deleteTable()
        except:
            print("Can't delete table or table does not exist")    
            
    def deleteDatabase(self) -> None:
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
        _createFile(self._generateDict(),name,indentVal)

    def AddTableFromJson(self,file : str) -> Table:
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