from .sql_interraction import *



def testTemplate(data,name) -> object:
    return Table(data,name,("id",int,True,True),("user",str,False,False),("email",str,False, False))