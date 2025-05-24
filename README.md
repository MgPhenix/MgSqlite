MgSqlite is module for create and interract with database without using sql, the module use sqlite3 but for create and interract with database you don't need to code in sql just use all the functions
This is an alpha version, it's just the basic function, the code is not really good either but i will improve it later

How to use :

create a database with myDatabase = Database("name")
it will automatically create a database file (".db") in your folder


Function currently available :
  createTable():
  
    create a Table in the database with all the parameter you want
    it take as parameter the name of your table and all the tuple for each columns you want 
    tuples are used like this : ("Name Of Collumn", type, primary key, autoincrement) -> type is just the type of date just put int, str or anything else, primary key is a boolean True if yes False if not, Same as primary autoincrement is a boolean
    exemple :  createTable("myTable",("id",int,True,True),("city",str,False,False))

  deleteIfTableExist():
  
    Pretty obvious but take as parameter the name of a table and delete if she exist, if not do nothing so it doesnt' crash programm don't worry

  selectFromTable():
  
    Select value from a table, take as parameter the name of the table, the column you want to get as result, and as much tuple as you want for check,
    exemple if you want to select the city when the id is equal to 0:
    selectFromTable("myTable",["price"],("id",0))     if you want to add if city = "Paris" just add it as a tuple :  selectFromTable("myTable",["price"],("id",0),("city","Paris")) 

  addValToTable():
  
    yeah pretty obvious too, just add a value to a table, take as parameter the name of the table, value to add as tuple and optional a list of column who will be modify 
    exemple:
    addValToTable("myTable",(0,"Paris"))  Follow the same order as your table, you can choose which columns will be modify : 
    addValToTable("myTable",("Paris"),("city")) Then id won't be set but if id is autoincrement he will be set

  simpleExecute():
  
    if you want to execute sql you can with this function take as parameter the sql code and optional a list of value if you use a SELECT
    simpleExecute("SELECT id FROM myTable WHERE city = 'Paris' ")


    
