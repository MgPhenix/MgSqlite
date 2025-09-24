import os
from .sql_interraction import SQL_Execution

class Database(SQL_Execution):
    def __init__(self, * ,name : str = "default") -> None:
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
        except:
            print("Can't delete database")