from MgSqlite.database import Database
from MgSqlite.table import Table

data = Database("")
table1 = Table(
    database = data,
    name = "table1",
    value = [("id",int,True,True),
             ("name",str,False,False)]
)
#data.turnOnPrintSQL()
table1.addValue(values = (None,"Jean"))
table1.addValue((None,"Timeo"))
print(table1.selectValues(["name"],("id",0,True)))
#print(data.tableList)
try:
    table1.updateValue([("name","George")],("id",0,True))
except Exception as e:
    print(e)
#print(table1.selectValues(["id","name"],("id",0,True)))
#print(table1.selectAll())
table1.show()
table1.deleteValue(("id",0,True))
table1.show()

