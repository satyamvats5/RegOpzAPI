from Helpers.DatabaseHelper import DatabaseHelper
from flask_restful import Resource,request
import Models.Resource as rsc
from Constants.Status import *
import json
from Helpers.utils import autheticateTenant
from Helpers.authenticate import *

class ResourceController(Resource):
    def __init__(self):
        self.domain_info = autheticateTenant()
        if self.domain_info:
            tenant_info = json.loads(self.domain_info)
            self.tenant_info = json.loads(tenant_info['tenant_conn_details'])
            self.dbhelper=DatabaseHelper(self.tenant_info)

    @authenticate
    def get(self,id=None):
        return rsc.Resource().get(id)


    def put(self,id=None):
        res=request.get_json(force=True)
        if id==None:
            return RESOURCE_EMPTY

        queryString="update resource set name=%s where id=%s"
        values=(res['name'],id)
        rowid=self.dbhelper.transact(queryString,values)
        self.dbhelper.commit()

        return rowid


    def post(self):
        res = request.get_json(force=True)

        queryString = "insert into resource(name) values(%s)"
        values = (res['name'],)
        rowid = self.dbhelper.transact(queryString, values)
        self.dbhelper.commit()
        return rowid

    def delete(self,id=None):
        if id == None:
            return RESOURCE_EMPTY

        queryString = "delete from resource where id=%s"
        values = (id,)
        rowid = self.dbhelper.transact(queryString, values)
        self.dbhelper.commit()
        return rowid
