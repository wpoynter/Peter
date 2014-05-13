#!/usr/bin/python

import datetime

class ResponseDomainAll(object):
	ID = 0
	def __init__(self, domain_id):
		ResponseDomainAll.ID += 1
		self.ID = ResponseDomainAll.ID
		self.domain_id = domain_id
		self.created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
		self.updated_at = self.created_at
