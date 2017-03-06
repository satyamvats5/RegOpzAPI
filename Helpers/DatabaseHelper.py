import mysql.connector
from Configs import dbconfig
class DatabaseHelper(object):
    def __init__(self):
        self.db = dbconfig.DATABASE['db'];
        self.host = dbconfig.DATABASE['host'];
        self.port = dbconfig.DATABASE['port'];
        self.user = dbconfig.DATABASE['user'];
        self.password = dbconfig.DATABASE['password'];
        self.type = dbconfig.DATABASE['type'];
        self.cnx = mysql.connector.connect(user=self.user, password=self.password, host=self.host,database=self.db)
        self.cursor = self.cnx.cursor()
    def query(self,queryString, queryParams=None):
        if queryParams != None:
            self.cursor.execute(queryString % queryParams)
        else:
            self.cursor.execute(queryString)
        return self.cursor
    def transact(self,queryString, queryParams=()):
        self.cursor.execute(queryString, queryParams)
        self.cnx.commit()
        return self.cursor.lastrowid
    def __del__(self):
        self.cursor.close()
        self.cnx.close()
