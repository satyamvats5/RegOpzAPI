from Helpers.DatabaseHelper import DatabaseHelper

class UserPermission(object):
    def __init__(self):
        pass

    def get(self, usedId=None):
        if userId:
            queryString = 'SELECT * FROM vUserPermissions WHERE username=%s'
            queryParams = (userId, )
            dbhelper = DatabaseHelper()
            permissions = dbhelper.query(queryString, queryParams)
            permissionList = permissions.fetchall()
            if len(permissionList) == 0:
                return { 'msg': 'No Permission Granted for this user' }
            self.role = permissionList[0]['role']
            self.permission = []
            for entry in permissionList:
                self.permission.append({ entry['component'] : entry['permission'] })
            return self.__dict__
        else:
            raise ValueError('UserId not specified!')