import MgSqlite


data = MgSqlite.Database()
table1 = MgSqlite.Table(
    database = data,
    name = "table1",
    value = [("id",int,True,True),
             ("name",str,False,False)]
)
data.turnOnPrintSQL()
table1.addValue(values = (0,"Jean"))
table1.addValue((1,"Timeo"))
print(table1.selectValues(["name"],("id",0)))
print(data.tableList)
try:
    table1.updateValue([("name","George")],("id",0))
except Exception as e:
    print(e)
print(table1.selectValues(["id","name"],("id",0)))
print(table1.selectAll())
table1.show()
data.deleteAllTable()
data.deleteDatabase()

