from MgSqlite import *


data = Database(name="test")
data.turnOnPrintSQL()


my_table = Table(name="table1",database=data,value=(
    ("id",int,True,True),
    ("name",str,False,False)
))

value = [
    (None,"Jean"),
    (None,"Pierre"),
    (None,"George")
]

my_table.addMultipleValues(value)

res = my_table.selectValues(["id","name"],{"column":"id","value":1,"condition":" AND ","sign" : "="})
print(res)

# version dico
# version tuple