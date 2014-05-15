#!/usr/bin/python

import datetime

class IfthenelseConstruct(object):
	ID = 0
	def __init__(self, textid, condition_text):
		IfthenelseConstruct.ID += 1
		self.ID = IfthenelseConstruct.ID
		self.textid = textid
		self.condition_text = condition_text
		self.children = []
		self.instances = []
		self.created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
		self.updated_at = self.created_at

        def cleanTextid(self, prefixLength):
                self.textid = "c_" + self.textid[prefixLength + 2:]

	def getLastInstace(self):
		return self.instances[-1]

	def getInstance(self, parent_id):
		for instance in self.instances:
			if instance.parent_id == parent_id:
				return instance
		return False

	def newInstance(self, parent_id, cc_all_id):
		self.instances.append(self.Instance(parent_id, cc_all_id, self.textid + "_" + str(len(self.instances)+1)))

	class Instance(object):
		sqlID = 0
		def __init__(self, parent_id, cc_all_id, textid):
			IfthenelseConstruct.Instance.sqlID += 1
			self.sqlID = IfthenelseConstruct.Instance.sqlID
			self.parent_id = parent_id
			self.cc_all_id = cc_all_id
			self.textid = textid
			self.position = 0
