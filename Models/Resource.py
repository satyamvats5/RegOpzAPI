from Helpers.DatabaseHelper import DatabaseHelper

class Resource(object):
    def __init__(self,params=None):
        if params:
            self.id=params['id']
            self.name=params['name']
        else:
            self.id=None
            self.name=None

    def add(self):
        dbhelper=DatabaseHelper()
        values=(self.id,self.name)
        queryString = "INSERT INTO resource(id, name) VALUES (%s, %s)"

        rowid = dbhelper.transact(queryString, values)
        self.get(rowid)

    def get(self,id=None):
        dbhelper=DatabaseHelper()

        if id:
            queryParams=(id,)
            queryString="select * from resource where id=%s"

            resources=dbhelper.query(queryString,queryParams)

            if resources.rowcount:
                role=resources.fetchone()
                self.id=resources['id']
                self.name=resources['name']
                return self.__dict__
            return None
        else:
            resourceslist=[]
            queryString="select * from resource"
            allresources=dbhelper.query(queryString)

            for rsc in allresources:
              resourceslist.append({'id':rsc['id'],'name':rsc['name']})

            return resourceslist

        return None


