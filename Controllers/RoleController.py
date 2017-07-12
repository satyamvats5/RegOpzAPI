from Helpers.DatabaseHelper import DatabaseHelper
from flask_restful import Resource,request
from Models.UserPermission import UserPermission
from Constants.Status import *

class RoleController(Resource):

    def get(self):
        return UserPermission().get()

    def post(self):
        res = request.get_json(force=True)
        return UserPermission().save(res)

    def delete(self, role=None):
        return UserPermission().remove(role)
