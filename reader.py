#!/usr/bin/python

import xml.etree.ElementTree as ET
import sys
import os.path
#from multiprocessing import Pool, Value
from functools import partial

from classes.question import Question
from classes.category import Category
from classes.code_scheme import CodeScheme
from classes.code import Code
from classes.variable_group import VariableGroup
import util 

class Parser(object):
	def __init__(self, infilename, np, defaults, silent=False):
		tree = ET.parse(infilename)
		self.np = np
		self.defaults = defaults
		Parser.silent = silent
		self.root = tree.getroot()
		""" Object arrays """
		self.questions = []
                self.instructions = []
		self.text_answers = []
		self.num_answers = []
		self.timedate_answers = []
		self.code_answers = []
		self.code_schemes = []
		self.categories = []
		self.variable_groups = {}

	def run(self):
		for grandad in self.root:
			if grandad.tag != '{http://www.icpsr.umich.edu/DDI}dataDscr':
				continue
			for dad in grandad:
				if dad.tag == '{http://www.icpsr.umich.edu/DDI}varGrp':
					self.readVarGrp(dad)
					continue
				if dad.tag == '{http://www.icpsr.umich.edu/DDI}var':
					for child in dad:
						if child.tag == '{http://www.icpsr.umich.edu/DDI}qstn':
							self.readVar(dad)
							break

	def readVarGrp(self, varGrp):
		label = ""
		for child in varGrp:
			if child.tag == '{http://www.icpsr.umich.edu/DDI}labl':
				label = child.text
		self.variable_groups[str(varGrp.attrib['ID'])] = VariableGroup(varGrp.attrib['ID'], label)
		if 'varGrp' in varGrp.attrib:
			self.variable_groups[str(varGrp.attrib['ID'])].memberGroups = varGrp.attrib['varGrp'].split()
		if 'var' in varGrp.attrib:
			self.variable_groups[str(varGrp.attrib['ID'])].memberVariables = varGrp.attrib['var'].split()
	
	def readVar(self, var):
		self.questions.append(Question(var.attrib['ID'], var.attrib['name']))
		catgryOrder = 0
		highest = 0
		lowest = 9999999
		max = None
		min = None
		for child in var:
			if child.tag == '{http://www.icpsr.umich.edu/DDI}labl':
				self.questions[-1].label = util.removeLineBreaks(child.text)
			if child.tag == '{http://www.icpsr.umich.edu/DDI}respUnit':
				self.questions[-1].respUnit = util.removeLineBreaks(child.text)
			if child.tag == '{http://www.icpsr.umich.edu/DDI}qstn':
				for gchild in child:
					if gchild.tag == '{http://www.icpsr.umich.edu/DDI}qstnLit':
						self.questions[-1].literal = util.removeLineBreaks(gchild.text)
					if gchild.tag == '{http://www.icpsr.umich.edu/DDI}ivuInstr':
						self.questions[-1].instruction = util.removeLineBreaks(gchild.text)
			if child.tag == '{http://www.icpsr.umich.edu/DDI}universe':
				self.questions[-1].universe = util.removeLineBreaks(child.text)
			if child.tag == '{http://www.icpsr.umich.edu/DDI}valrng':
				for gchild in child:
					if gchild.tag == '{http://www.icpsr.umich.edu/DDI}range':
						max = gchild.attrib['max']
						min = gchild.attrib['min']
			if child.tag == '{http://www.icpsr.umich.edu/DDI}catgry':
				labl = ""
				catValu = ""
				for gchild in child:
					if gchild.tag == '{http://www.icpsr.umich.edu/DDI}labl':
						labl = gchild.text
					if gchild.tag == '{http://www.icpsr.umich.edu/DDI}catValu':
						catValu = gchild.text
						try:
							val = float(catValu)
							if val > highest:
								highest = val
							if val < lowest:
								lowest = val
						except ValueError:
							pass
				if labl == "" or catValu == "":
					continue
				self.code_answers.append(Code(catValu,catgryOrder))
				if len(filter(lambda x: x.label == labl, self.categories)) > 0:
					for i in range(len(self.categories)):
						if self.categories[i].label == labl:
							self.code_answers[-1].category_id = self.categories[i].ID 
							break
				else:
					self.categories.append(Category(labl))
					self.code_answers[-1].category_id = self.categories[-1].ID
				if len(filter(lambda x: x.label == 'cs_'+var.attrib['ID'], self.code_schemes)) > 0:
					for i in range(len(self.code_schemes)):
						if self.code_schemes[i].label == 'cs_'+var.attrib['ID']:
							self.code_answers[-1].code_scheme_id = self.code_schemes[i].ID
							self.code_schemes[i].codes.append(self.code_answers[-1])
							break
				else:
					self.code_schemes.append(CodeScheme('cs_'+var.attrib['ID']))
					self.code_answers[-1].code_scheme_id = self.code_schemes[-1].ID
					self.code_schemes[-1].codes.append(self.code_answers[-1])
				self.questions[-1].code_scheme_id = self.code_schemes[-1].ID
				catgryOrder += 1

	def clean(self):
		if not Parser.silent: print "Cleaning code schemes"
		toRemove = [None] * len(self.code_schemes)
		for i in range(len(self.code_schemes)):
                        toRemove[i] = scanner(i, self)
		"""pool = Pool(processes=self.np)
		coupled_scanner = partial(scanner, obj=self)
		toRemove = pool.map(coupled_scanner, range(len(self.code_schemes)))"""
			
		if not Parser.silent: print ""
		temp = []
		for index in range(len(self.code_schemes)):

			if self.code_schemes[index].ID != toRemove[index]:
				temp_code_answers = [x for x in self.code_answers if x.code_scheme_id != self.code_schemes[index].ID]
				self.code_answers = temp_code_answers
				"""for code_answer in self.code_answers:
					if code_answer.code_scheme_id == self.code_schemes[index].ID:
						self.code_answers.remove(code_answer)
						print "=== Code Removed ===" """
				for question in self.questions:
					if question.code_scheme_id == self.code_schemes[index].ID:
						question.code_scheme_id = toRemove[index]

			else:
				temp.append(self.code_schemes[index])
		self.code_schemes = temp

        def separateInstructions(self):
                if not Parser.silent: print "Separating instructions from questions"
                reuses = 0
                for question in self.questions:
                        if question.instruction == None: continue
                        for instruction in self.instructions:
                                if instruction.text == question.instruction:
                                        instruction.uses += 1
                                        reuses += 1
                                        question.instruction = instruction.ID
                                        break
                        if type(question.instruction) is int: continue
                        self.instructions.append(Instruction(question.instruction))
                        question.instruction = self.instructions[-1].ID
                if not Parser.silent: print str(len(self.instructions)) + " instructions created"
                if not Parser.silent: print "With " + str(reuses) + " reused"


	def validate(self):
		if not Parser.silent: print "Validating data"
		missingRespUnit = 0
		respUnits = {}
		for question in self.questions:
			if question.respUnit == None:
				missingRespUnit += 1
			else:
				if question.respUnit in respUnits:
					respUnits[question.respUnit] += 1
				else:
					respUnits[question.respUnit] = 1
		if missingRespUnit > 0:
			if len(respUnits) > 0:
				highest = {"key": "none", "value": 0}
				for key in respUnits:
					if respUnits[key] > highest["value"]:
						highest["value"] = respUnits[key]
						highest["key"] = key
				if not Parser.silent: print "Not all of the questions have a response unit (interviewee) asigned."
				if not Parser.silent: print "The most common response unit that has been assgined is " + str(highest["key"])
				if self.defaults:
					self.applyRespUnitDefault(str(highest["key"]))
				else:
					response = raw_input("Would you like to use this as a default for all questions that are missing a response unit? (Y/n) ")
					if util.ifYes(response,"y"):
						self.applyRespUnitDefault(str(highest["key"]))
					else:
						response = raw_input("Would you like to enter a reponse unit for the remain questions?(Y/n) ")
						if util.ifYes(response,"y"):
							response = raw_input("Please enter the default reponse unit: (spaces allowed) (default:'default') ")
							self.applyRespUnitDefault(response)
						else:
							if not Parser.silent: print "<-- Continueing without ordering questions -->"
			else:
				if not Parser.silent: print "No questions have been asigned a response unit (interviewee).If a question does not have a response unit it can not be represented by a question construct."
				if self.defaults:
					self.applyRespUnitDefault('default')
				else:
					response = raw_input("Would you like to set a response unit for all the questions? (Y/n) ")
					if util.ifYes(response,"y"):
						response = raw_input("Please enter the default reponse unit: (spaces allowed) (default:'default') ")
						self.applyRespUnitDefault(response)
					else:
						if not Parser.silent: print "<-- Continueing without ordering questions -->"

	def applyRespUnitDefault(self, default):
		if default == "":
			respUnit = "default"
		else:
			respUnit = default
		for question in self.questions:
			if question.respUnit == None:
				question.respUnit = respUnit

	def getData(self):
		data = {}
		data['questions'] = self. questions
		data['categories'] = self.categories
		data['code_schemes'] = self.code_schemes
		data['code_answers'] = self.code_answers
		data['variable_groups'] = self.variable_groups
		return data

	def output(self):
		if not Parser.silent: print "No. of question objects: " + str(len(self.questions))
		if not Parser.silent: print "No. of category objects: " + str(len(self.categories))
		if not Parser.silent: print "No. of code scheme objects: " + str(len(self.code_schemes))
		if not Parser.silent: print "No. of code objects: " + str(len(self.code_answers))
		#for question in self.questions:
		#	question.output()

def scanner(i, obj):
	if not Parser.silent: print "Progress: " + str(i+1) + "/" + str(len(obj.code_schemes)) + "\r",
	sys.stdout.flush()
	code_answers_alpha = obj.code_schemes[i].codes
	#code_answers_alpha = filter(lambda x: x.code_scheme_id == i, obj.code_answers)
	for j in range(i):
		code_answers_beta = obj.code_schemes[j].codes
		#code_answers_beta = filter(lambda x: x.code_scheme_id == j, obj.code_answers)
		if len(code_answers_alpha) != len(code_answers_beta):
			continue	
		identicals = 0
		for alpha in code_answers_alpha:
			for beta in code_answers_beta:
				if alpha.category_id != beta.category_id:
					continue
				if alpha.cs_value != beta.cs_value:
					continue
				if alpha.cs_order != beta.cs_order:
					continue
				identicals += 1
		if identicals >= len(code_answers_alpha):

			return obj.code_schemes[j].ID
	return obj.code_schemes[i].ID
