#!/usr/bin/python

import datetime

class ResponseDomainCode(object):
	ID = 0
	def __init__(self, code_scheme_id):
		ResponseDomainCode.ID += 1
		self.ID = ResponseDomainCode.ID
		self.code_scheme_id = code_scheme_id
		self.created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
		self.updated_at = self.created_at
