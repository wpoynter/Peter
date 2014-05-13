#!/usr/bin/python

import datetime

class Category(object):
	ID = 0
	def __init__(self, label):
		Category.ID += 1
		self.ID = Category.ID
		self.label = label
		self.created_at = datetime.datetime.now().strftime("%H:%M:%S")
		self.updated_at = self.created_at
