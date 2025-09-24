from .table import Table

class Column:
    def __init__(self,colType,isPrimaryKey=False,isAutoincrement=False):
        self.colType = colType
        self.isPrimaryKey = isPrimaryKey
        self.isAutoincrement = isAutoincrement

class Integer(Column):
    def __init__(self,isPrimaryKey=False,isAutoincrement=False):
        super().__init__("INTEGER",isPrimaryKey,isAutoincrement)

class String(Column):
    def __init__(self):
        super().__init__("TEXT")

class Model(Table):
    
    def save(self,db):
        dict = self.__dict__
        db = dict["database"]
        name = dict["table_name"]
        columns = []
        del dict["table_name"]
        del dict["database"]
        result = f"CREATE TABLE IF NOT EXISTS {name}("
        for key, value in dict.items():
            columns.append(str(key))
            result+= str(key) + " " + value.colType
            if value.isPrimaryKey:
                result+=" PRIMARY KEY"
            if value.isAutoincrement:
                result+=" AUTOINCREMENT"
            result+=","
        result=result[:-1] + ")"
        
        self.database = db
        self.database.tableList.append(self)
        print(self.database.tableList)
        self.name = name
        self.columns = columns
        self.simpleExecute(self.database,result)