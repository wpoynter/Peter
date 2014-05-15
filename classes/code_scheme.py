#!/usr/bin/python

import datetime

class CodeScheme(object):
	ID = 0
	def __init__(self, label):
		CodeScheme.ID += 1
		self.ID = CodeScheme.ID
		self.label = label
		self.sqlID = None
		self.codes = []
		self.created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
		self.updated_at = self.created_at

        def cleanLabel(self, prefixLength):
                self.label = "cs_" + self.label[prefixLength + 3:]

