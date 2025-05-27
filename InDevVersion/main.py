from MgSqlite import *
import os


def deleteDatabase(name):
     try:
         os.remove(name+".db")
     except:
         name.delete(). #not implement yet 

