import sqlite3


class SQL_Execution:

    def simpleExecute(self,database : object, command : str, list : list = []) -> tuple:                  #Function for execute One command in sqlite3, just to shorten the code
        """
        Execute sql script, return a value if the command is a selection return None if not
        """
        try:
            conn = sqlite3.connect(database.databaseName)
        except:
            print("Error : can't connect to the database")

        cur = conn.cursor()
        try:                                                                        
            res = cur.execute(command,list)                                                             # I doesn't like this line because it just repeat the same line 2 time, but it's necessary because when you don't do a SELECT for getting a result you don't have a list to put as parameter      edit : Nevermind i found how to fix that
        except:
            print("Error : can't execute command")

        res = res.fetchall()
        conn.commit()
        conn.close()
        if len(res)>=1:
            return res[0]

    def tryConnect(self,databaseName) -> None:
        try:
            conn = sqlite3.connect(databaseName)
            conn.close()
        except:
            print("Error : Incorrect Name")