#!/usr/bin/python

import xml.etree.ElementTree as ET

from classes.question import Question

class Parser(object):
	def __init__(self, filename):
		self.tree = ET.parse(filename)
		self.root = self.tree.getroot()
		""" Object arrays """
		self.questions = []
		self.question_items = []
		self.question_construct = []
		self.universes = []
		self.conditions = []
		self.sequences = []
		self.statements = []
		self.text_answers = []
		self.num_answers = []
		self.timedate_answers = []
		self.code_answers = []
		self.code_schemes = []
		self.categories = []

	def run(self):
		
		for grandad in self.root:
			if grandad.tag != 'dataDscr':
				continue
			for dad in grandad:
				if dad.tag != 'var':
					continue
				for child in dad:
					if child.tag == 'qstn':
						self.readVar(dad)
						break
	
	def readVar(self, var):
		self.questions.append(Question(var.attrib['ID'], var.attrib['name']))
		for child in var:
			if child.tag == 'labl':
				self.questions[-1].label = child.text
			if child.tag == 'qstn':
				for gchild in child:
					if gchild.tag == 'qstnLit':
						self.questions[-1].literal = child.text
					if gchild.tag == 'ivuInstr':
						self.questions[-1].instruction = child.text
