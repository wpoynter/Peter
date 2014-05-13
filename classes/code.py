#!/usr/bin/python

import datetime

class Code(object):
	ID = 0
	def __init__(self, cs_value, cs_order):
		Code.ID += 1
		self.ID = Code.ID
		self.sqlID = None
		self.code_scheme_id = -1
		self.category_id = -1
		self.cs_value = cs_value
		self.cs_order = cs_order
		self.created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
		self.updated_at = self.created_at

	def getInsert():
		pass

