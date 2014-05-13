#!/usr/bin/python

import datetime

class ResponseUnit(object):
	ID = 0
	def __init__(self, text):
		ResponseUnit.ID += 1
		self.ID = ResponseUnit.ID
		self.text = text
		self.created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
		self.updated_at = self.created_at
