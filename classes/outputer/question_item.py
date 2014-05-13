#!/usr/bin/python

import datetime

class QuestionItem(object):

	def __init__(self, ID, label, literal):
		self.ID = ID
		self.textid = "qi_" + str(self.ID)
		self.label = label
		self.literal = literal
		self.created_at = datetime.datetime.now().strftime("%H:%M:%S")
		self.updated_at = self.created_at

	def output (self):
		print self.ID + " " + self.name
		if self.label != None:
			print "\tLabel: " + self.label
		if self.literal != None:
			print "\tLiteral: " + self.literal
		if self.instruction != None:
			print "\tInstruction: " + self.instruction
		if self.universe != None:
			print "\tUniverse: " + self.universe
