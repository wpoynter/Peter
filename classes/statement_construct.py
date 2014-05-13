#!/usr/bin/python

import datetime

class StatementConstruct(object):
	ID = 0
	def __init__(self, textid, statement_item):
		StatementConstruct.ID += 1
		self.ID = StatementConstruct.ID
		self.textid = textid
		self.statement_item = statement_item
		self.parentless = True
		self.created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
		self.updated_at = self.created_at
