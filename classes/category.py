#!/usr/bin/python

import datetime

class Category(object):
	ID = 0
	def __init__(self, label):
		Category.ID += 1
		self.ID = Category.ID
		self.label = label
		self.sqlID = None
		self.created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
		self.updated_at = self.created_at
	
	def getInsert():
		pass
