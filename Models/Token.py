from Helpers.DatabaseHelper import DatabaseHelper
from Models.UserPermission import UserPermission
import uuid
from datetime import datetime, timedelta
from jwt import JWT, jwk_from_pem
from flask import request
from Constants.Status import *

class Token(object):
	def __init__(self):
		pass

	def create(self, user_id):
		try:
			self.tokenId = self.get(user_id)
		except ValueError:
			self.tokenId = str(uuid.uuid4())
			self.lease_start = datetime.now()
			self.lease_end = self.lease_start + timedelta(hours=24)
			self.ip = request.remote_addr
			self.user_agent = request.headers.get('User-Agent')
			self.user_id = user_id
			dbhelper = DatabaseHelper()
			queryString = "INSERT INTO token(token, lease_start, lease_end, ip, user_agent, user_id) VALUES (%s,%s,%s,%s,%s,%s)"
			values = (self.tokenId, self.lease_start, self.lease_end, self.ip, self.user_agent, self.user_id, )
			try:
				rowid = dbhelper.transact(queryString, values)
			except Exception:
				return NO_USER_FOUND
		user_permission = UserPermission().get(user_id)
		if user_permission:
			user = {
				'tokenId': self.tokenId,
				'userId': user_id,
				'role': user_permission['role'],
				'permission': user_permission['permission']
			}
			jwtObject = JWT()
			with open('private_key', 'rb') as fh:
				salt = jwk_from_pem(fh.read())
			jwt = jwtObject.encode(user, salt, 'RS256')
			#with open('public_key', 'r') as ft:
				#key = jwk_from_pem(ft.read().encode())
			#test = jwtObject.decode(jwt, key)
			#print(test['tokenId'])
			return jwt
		else:
			return { "msg": "Permission Denied" },301

	def get(self, userId):
		dbhelper = DatabaseHelper()
		queryString = "SELECT token FROM token WHERE user_id=%s and lease_end > %s"
		queryParams = (userId, datetime.now(), )
		cur = dbhelper.query(queryString, queryParams)
		data = cur.fetchone()
		if data:
			return data['token']
		else:
			raise ValueError("User not logged in!")

	def authenticate(self, token):
		extracted_token = token.replace("Bearer ","")
		with open('public_key', 'r') as fh:
			salt = jwk_from_pem(fh.read().encode())
		try:
			token_decode = JWT().decode(extracted_token, salt)
		except Exception:
			raise ValueError("Invalid Token Recieved for Authentication")
		dbhelper = DatabaseHelper()
		queryString = "SELECT * FROM token WHERE token=%s AND lease_end > %s"
		queryParams = (token_decode['tokenId'], datetime.now(), )
		cur = dbhelper.query(queryString, queryParams)
		data = cur.fetchone()
		if data and data['user_id'] == token_decode['userId']:
			return data['user_id']
		raise ValueError("Invalid Credentials Recieved for Authentication")
