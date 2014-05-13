#!/usr/bin/python

import datetime

class VariableGroup(object):
	ID = 1 
	def __init__(self, ID, textid):
		VariableGroup.ID += 1
		self.sqlID = VariableGroup.ID
		self.ID = ID
		self.textid = textid
		self.memberGroups = []
		self.memberVariables = []
		self.linked = False
		self.inserted = False
		self.parentless = True
		self.created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
		self.updated_at = self.created_at
