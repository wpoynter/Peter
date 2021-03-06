#!/usr/bin/python

import datetime

class CodeScheme(object):
	ID = 0
	def __init__(self, label):
		CodeScheme.ID += 1
		self.ID = CodeScheme.ID
		self.label = label
		self.created_at = datetime.datetime.now().strftime("%H:%M:%S")
		self.updated_at = self.created_at
