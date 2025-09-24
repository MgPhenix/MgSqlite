from MgSqlite import *

data = Database(name="Fleury_nichon")
my_table = Table(
    name="Jambon",
    database=data,
    value=(
    ("id",int,True,True),
    ("name",str,False,False)
))

value = [
    (None,"Jean"),
    (None,"Pierre"),
    (None,"George")
]

my_table.addMultipleValues(value)

res = my_table.selectValues(["id","name"],where="id >= 0 and name = 'Pierre'")
print(res)