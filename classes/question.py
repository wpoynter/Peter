#!/usr/bin/python

import datetime

class Question(object):

	def __init__(self, ID, name):
		self.ID = ID
		self.name = name
		self.sqlID = None
		self.label = None
		self.literal = None
		self.instruction = None
		self.universe = None
		self.code_scheme_id = None
		self.respUnit = None
		self.numeric = None
		self.created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
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

	class Numeric(object):
		def __init__(self, high, low):
			self.high = high
			self.low = low
