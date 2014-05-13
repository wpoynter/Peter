#!/usr/bin/python

class Setup(object):
	def __init__(self, filename):
		self.f = open(filename, 'r')

	def get(self):
		return f.read()
