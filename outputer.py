#!/usr/bin/python

from __future__ import with_statement
import datetime

from classes.response_domain_code import ResponseDomainCode
from classes.response_domain_all import ResponseDomainAll
from classes.response_unit import ResponseUnit
from classes.question_construct import QuestionConstruct
from classes.ifthenelse_construct import IfthenelseConstruct

class Outputer(object):
	def __init__(self, data, silent=False):
		self.data = data
		Outputer.silent = silent
		self.ids = {}
		self.question_items = []
		self.categories = []
		self.code_schemes = []
		self.codes = []
		self.response_domain_alls = []
		self.response_domain_codes = []
		self.response_domain_datetimes = []
		self.response_domain_numerics = []
		self.response_domain_texts = []
		self.response_domain_types = []
		self.question_constructs = []
		self.response_units = []
		self.sequence_constructs = []
		self.statement_constructs = []
		self.ifthenelse_constructs = []

	def prepareString(self, inputStr):
		output = "NULL"
		if inputStr != None:
			output = '"' + inputStr.encode('utf-8').replace('"', '""') + '"'
		return output

	def resetIDs(self):
		self.ids['question_items'] = 0
		self.ids['code_schemes'] = 0
		self.ids['categories'] = 0
		self.ids['codes'] = 0
		self.ids['response_domain_codes'] = 0
		self.ids['response_domain_alls'] = 0
		self.ids['qi_rdas'] = 0
		self.ids['response_units'] = 0
		self.ids['cc_questions'] = 0
		self.ids['cc_alls'] = 1
		self.ids['cc_statements'] = 0

	def write(self, filename):
		self.resetIDs()
		if not Outputer.silent: print "<-- Opening file: " + filename + " -->"
		with open(filename, 'w') as f:
			if not Outputer.silent: print "<-- Writing to file: " + filename + " -->"
			f.write('-- SQL file to be loaded into Caddies')
			f.write('\n')
			if not Outputer.silent: print "<-- Writing question data -->"
			self.writeQuestionData(f)
			if not Outputer.silent: print "<-- Writing sequence data -->"
			self.writeSequenceData(f)
	
	def writeQuestionData(self,f):
                currentTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                for instruction in self.data['instructions']:
                        f.write('INSERT INTO instructions (id, instruction_text, created_at, updated_at) VALUES ')
                        f.write('(' + str(instruction.ID)  + ',' + self.prepareString(instruction.text) + ',"' + str(currentTime) + '","' + str(currentTime) + '")')
                        f.write(';\n')
		prevQuestion = None
		for question in self.data['questions']:
			self.ids['question_items'] += 1
                        f.write('INSERT INTO question_items (id, textid, literal, intent, created_at, updated_at, instruction_id) VALUES ')
			f.write('(' + str(self.ids['question_items'])  + ',"qi_' + str(question.ID) + '",')
			if question.literal == None:
				f.write(self.prepareString(question.label))
			else:
				f.write(self.prepareString(question.literal))
                        f.write(',' + self.prepareString(question.label) + ',"' + str(question.created_at) + '","' + str(question.updated_at) + '",' + str(question.instruction) + ')')
			f.write(';\n')
			question.sqlID = self.ids['question_items']
			respUnits = [x for x in self.response_units if x.text == question.respUnit]
			if len(respUnits) == 0:
				self.ids['response_units'] += 1
				f.write('INSERT INTO response_units (id, text, created_at, updated_at) VALUES ')
				f.write('(' + str(self.ids['response_units'])  + ',"' + str(question.respUnit) + '","' + str(question.created_at) + '","' + str(question.updated_at) + '")')
				f.write(';\n')
				self.response_units.append(ResponseUnit(question.respUnit))
				respUnitSqlID = self.ids['response_units']
				self.response_units[-1].sqlID = self.ids['response_units']
			else:
				respUnitSqlID = respUnits[0].sqlID
			self.ids['cc_questions'] += 1
                        f.write('INSERT INTO cc_questions (id, textid, question_reference_id, response_unit_id, created_at, updated_at, question_reference_type) VALUES ')
                        f.write('(' + str(self.ids['cc_questions'])  + ',"qc_' + str(question.ID) + '",' + str(question.sqlID)  + ',' + str(respUnitSqlID) + ',"' + str(question.created_at) + '","' + str(question.updated_at) + '","QuestionItem")')
			f.write(';\n')
			self.question_constructs.append(QuestionConstruct('qc_' + str(question.ID), question.sqlID, respUnitSqlID))
			self.question_constructs[-1].sqlID = self.ids['cc_questions']
			for code_scheme in self.data['code_schemes']:
				if code_scheme.ID == question.code_scheme_id:
					if code_scheme.sqlID == None:
						self.ids['code_schemes'] += 1
						f.write('INSERT INTO code_schemes (id, label, created_at, updated_at) VALUES ')
						f.write('(' + str(self.ids['code_schemes']) + ',' + self.prepareString(code_scheme.label) + ',"' + str(code_scheme.created_at) + '","' + str(code_scheme.updated_at) + '")')
						f.write(';\n')
						code_scheme.sqlID = self.ids['code_schemes']
						self.ids['response_domain_codes'] += 1
						self.response_domain_codes.append(ResponseDomainCode(code_scheme.ID))
						self.response_domain_codes[-1].code_scheme_sqlID = code_scheme.sqlID
						f.write('INSERT INTO response_domain_codes (id, code_scheme_id, created_at, updated_at) VALUES ')
						f.write('(' + str(self.ids['response_domain_codes']) + ',' + str(code_scheme.sqlID) + ',"' + str(code_scheme.created_at) + '","' + str(code_scheme.updated_at) + '")')
						f.write(';\n')
						self.response_domain_codes[-1].sqlID = self.ids['response_domain_codes']
						self.ids['response_domain_alls'] += 1
						self.response_domain_alls.append(ResponseDomainAll(self.response_domain_codes[-1].ID))
						self.response_domain_alls[-1].response_domain_codes_sqlID = self.response_domain_codes[-1].sqlID
						f.write('INSERT INTO response_domain_alls (id, response_domain_type_id, domain_id, created_at, updated_at, domain_type) VALUES ')
						f.write('(' + str(self.ids['response_domain_alls']) + ',3,' + str(self.response_domain_codes[-1].sqlID) + ',"' + str(code_scheme.created_at) + '","' + str(code_scheme.updated_at) + '","ResponseDomainCode")')
						f.write(';\n')
						self.response_domain_alls[-1].sqlID = self.ids['response_domain_alls']
						self.ids['qi_rdas'] += 1
						f.write('INSERT INTO qi_rdas (id, question_item_id, response_domain_all_id, created_at, updated_at) VALUES ')
						f.write('(' + str(self.ids['qi_rdas']) + ',' + str(question.sqlID) + ',' + str(self.response_domain_alls[-1].sqlID) + ',"' + str(code_scheme.created_at) + '","' + str(code_scheme.updated_at) + '")')
						f.write(';\n')
						codes = filter((lambda x: x.code_scheme_id == code_scheme.ID), self.data['code_answers'])
						for code in codes:
							for category in self.data['categories']:
								if code.category_id == category.ID:
									if category.sqlID == None:
										self.ids['categories'] += 1
										f.write('INSERT INTO categories (id, label, created_at, updated_at) VALUES ')
										f.write('(' + str(self.ids['categories']) + ',' + self.prepareString(category.label) + ',"' + str(category.created_at) + '","' + str(category.updated_at) + '")')
										f.write(';\n')
										category.sqlID = self.ids['categories']

									else:
										break
							self.ids['codes'] += 1
							f.write('INSERT INTO codes (id, code_scheme_id, category_id, cs_value, cs_order, created_at, updated_at) VALUES ')
							f.write('(' + str(self.ids['codes']) + ',' + str(code_scheme.sqlID) + ',' + str(filter((lambda x: x.ID == code.category_id), self.data['categories'])[0].sqlID) + ',' + self.prepareString(code.cs_value) + ',' + str(code.cs_order) + ',"' + str(category.created_at) + '","' + str(category.updated_at) + '")')
							f.write(';\n')
							code.sqlID = self.ids['codes']
					else:
						self.ids['qi_rdas'] += 1
						response_domain_code_id = [x.ID for x in self.response_domain_codes if x.code_scheme_id == question.code_scheme_id][0]
						response_domain_all_sqlID = [y.sqlID for y in self.response_domain_alls if y.domain_id == response_domain_code_id][0]
						f.write('INSERT INTO qi_rdas (id, question_item_id, response_domain_all_id, created_at, updated_at) VALUES ')
						f.write('(' + str(self.ids['qi_rdas']) + ',' + str(question.sqlID) + ',' + str(response_domain_all_sqlID) + ',"' + str(code_scheme.created_at) + '","' + str(code_scheme.updated_at) + '")')
						f.write(';\n')
			if question.universe != None:
				new = True
				for ifthenelse in self.ifthenelse_constructs:
					if ifthenelse.condition_text == question.universe:
						new = False
						ifthenelse.children.append(self.question_constructs[-1].sqlID)
				if new:
					self.ifthenelse_constructs.append(IfthenelseConstruct('c_q'+str(prevQuestion.ID), question.universe))
					self.ifthenelse_constructs[-1].children.append(self.question_constructs[-1].sqlID)
			prevQuestion = question
						
	def writeSequenceData(self,f):
		f.write('-- Sequence data\n')
		#Find parentless constructs
		for statement in self.statement_constructs:
			for vg_key, vg_val in self.data['variable_groups'].iteritems():
				for memberVariable in vg_val.memberVariables:
					if statement.textid == 's_q' + memberVariable:
						statement.parentless = False
						break
				if not statement.parentless:
					break
		for question in self.question_constructs:
			for vg_key, vg_val in self.data['variable_groups'].iteritems():
				for memberVariable in vg_val.memberVariables:
					if question.textid == 'qc_' + memberVariable:
						question.parentless = False
						break
				if  not question.parentless:
					break
		for varGrp_key, varGrp_val in self.data['variable_groups'].iteritems():
			for vg_key, vg_val in self.data['variable_groups'].iteritems():
				for memberGroup in vg_val.memberGroups:
					if varGrp_val.ID == memberGroup:
						varGrp_val.parentless = False
						break
				if not varGrp_val.parentless:
					break
		
		position = 0
		for question in self.question_constructs:
			if question.parentless:
				self.ids['cc_alls'] += 1
				position += 1
				inserted = False
				for ifthenelse in self.ifthenelse_constructs:
					for child in ifthenelse.children:
						if question.sqlID == child:
							if not ifthenelse.getInstance(1):
								ifthenelse.newInstance(1, self.ids['cc_alls'])
								f.write('INSERT INTO cc_ifthenelses (id, textid, condition, created_at, updated_at) VALUES ')
								f.write('(' + str(ifthenelse.getLastInstace().sqlID)  + ',"' + ifthenelse.getLastInstace().textid + '",' + self.prepareString(ifthenelse.condition_text) + ',"' + str(ifthenelse.created_at) + '","' + str(ifthenelse.updated_at) + '")')
								f.write(';\n')
								f.write('INSERT INTO cc_alls (id, construct_type, construct_id, created_at, updated_at, parent_id, position, ifbranch) VALUES ')
								f.write('(' + str(ifthenelse.getLastInstace().cc_all_id)  + ',"CcIfthenelse",' + str(ifthenelse.getLastInstace().sqlID) + ',"' + str(ifthenelse.created_at) + '","' + str(ifthenelse.updated_at) + '",' + str(ifthenelse.getLastInstace().parent_id) + ',' + str(position) + ',"f")')
								f.write(';\n')
								self.ids['cc_alls'] += 1
							ifthenelse.getLastInstace().position += 1
							f.write('INSERT INTO cc_alls (id, construct_type, construct_id, created_at, updated_at, parent_id, position, ifbranch) VALUES ')
							f.write('(' + str(self.ids['cc_alls'])  + ',"CcQuestion",' + str(question.sqlID) + ',"' + str(question.created_at) + '","' + str(question.updated_at) + '",' + ifthenelse.getInstance(1).cc_all_id + ',' + str(ifthenelse.getInstance(1).position) + ',"t")')
							f.write(';\n')
							inserted = True
							break
					if inserted:
						break
				if not inserted:
					f.write('INSERT INTO cc_alls (id, construct_type, construct_id, created_at, updated_at, parent_id, position, ifbranch) VALUES ')
					f.write('(' + str(self.ids['cc_alls'])  + ',"CcQuestion",' + str(question.sqlID) + ',"' + str(question.created_at) + '","' + str(question.updated_at) + '",1,' + str(position) + ',"f")')
					f.write(';\n')
					
		for statement in self.statement_constructs:
			if statement.parentless:
				self.ids['cc_alls'] += 1
				position += 1
				f.write('INSERT INTO cc_alls (id, construct_type, construct_id, created_at, updated_at, parent_id, position, ifbranch) VALUES ')
				f.write('(' + str(self.ids['cc_alls'])  + ',"CcStatement",' + str(statement.sqlID) + ',"' + str(statement.created_at) + '","' + str(statement.updated_at) + '",1,' + str(position) + ',"f")')
				f.write(';\n')
				
		for varGrp_key, varGrp_val in self.data['variable_groups'].iteritems():
			if varGrp_val.parentless:
				f.write('INSERT INTO cc_sequences (id, textid, created_at, updated_at) VALUES ')
				f.write('(' + str(varGrp_val.sqlID)  + ',' + self.prepareString(varGrp_val.textid) + ',"' + str(varGrp_val.created_at) + '","' + str(varGrp_val.updated_at) + '")')
				f.write(';\n')
				
				self.ids['cc_alls'] += 1
				position += 1
				f.write('INSERT INTO cc_alls (id, construct_type, construct_id, created_at, updated_at, parent_id, position, ifbranch) VALUES ')
				f.write('(' + str(self.ids['cc_alls'])  + ',"CcSequence",' + str(varGrp_val.sqlID) + ',"' + str(varGrp_val.created_at) + '","' + str(varGrp_val.updated_at) + '",1,' + str(position) + ',"f")')
				f.write(';\n')
				varGrp_val.inserted = True
				varGrp_val.cc_all_ID = self.ids['cc_alls']
				
		keepGoing = True
		while keepGoing:
			keepGoing = False
			for varGrp_key, varGrp_val in self.data['variable_groups'].iteritems():
				if varGrp_val.inserted and not varGrp_val.linked:
					keepGoing = True
					position = 0
					for memberGroup in varGrp_val.memberGroups:
						for vg_key, vg_val in self.data['variable_groups'].iteritems():
							if memberGroup == vg_val.ID:
								self.ids['cc_alls'] += 1
								position += 1
								f.write('INSERT INTO cc_sequences (id, textid, created_at, updated_at) VALUES ')
								f.write('(' + str(vg_val.sqlID)  + ',' + self.prepareString(vg_val.textid) + ',"' + str(vg_val.created_at) + '","' + str(vg_val.updated_at) + '")')
								f.write(';\n')
								f.write('INSERT INTO cc_alls (id, construct_type, construct_id, created_at, updated_at, parent_id, position, ifbranch) VALUES ')
								f.write('(' + str(self.ids['cc_alls'])  + ',"CcSequence",' + str(vg_val.sqlID) + ',"' + str(vg_val.created_at) + '","' + str(vg_val.updated_at) + '",' + str(varGrp_val.cc_all_ID) + ',' + str(position) + ',"f")')
								f.write(';\n')
								vg_val.cc_all_ID = self.ids['cc_alls']
								vg_val.inserted = True
								break
					for memberVariable in varGrp_val.memberVariables:
						for question in self.question_constructs:
							if 'qc_' + memberVariable == question.textid:
								inserted = False
								position += 1
								for ifthenelse in self.ifthenelse_constructs:
									for child in ifthenelse.children:
										if question.sqlID == child:
											if not ifthenelse.getInstance(varGrp_val.cc_all_ID):
												self.ids['cc_alls'] += 1
												ifthenelse.newInstance(varGrp_val.cc_all_ID, self.ids['cc_alls'])
												f.write('INSERT INTO cc_ifthenelses (id, textid, condition, created_at, updated_at) VALUES ')
												f.write('(' + str(ifthenelse.getLastInstace().sqlID)  + ',"' + ifthenelse.getLastInstace().textid + '",' + self.prepareString(ifthenelse.condition_text) + ',"' + str(ifthenelse.created_at) + '","' + str(ifthenelse.updated_at) + '")')
												f.write(';\n')
												f.write('INSERT INTO cc_alls (id, construct_type, construct_id, created_at, updated_at, parent_id, position, ifbranch) VALUES ')
												f.write('(' + str(ifthenelse.getLastInstace().cc_all_id)  + ',"CcIfthenelse",' + str(ifthenelse.getLastInstace().sqlID) + ',"' + str(ifthenelse.created_at) + '","' + str(ifthenelse.updated_at) + '",' + str(ifthenelse.getLastInstace().parent_id) + ',' + str(position) + ',"f")')
												f.write(';\n')
											ifthenelse.getLastInstace().position += 1
											self.ids['cc_alls'] += 1
											f.write('INSERT INTO cc_alls (id, construct_type, construct_id, created_at, updated_at, parent_id, position, ifbranch) VALUES ')
											f.write('(' + str(self.ids['cc_alls'])  + ',"CcQuestion",' + str(question.sqlID) + ',"' + str(question.created_at) + '","' + str(question.updated_at) + '",' + str(ifthenelse.getInstance(varGrp_val.cc_all_ID).cc_all_id) + ',' + str(ifthenelse.getInstance(varGrp_val.cc_all_ID).position) + ',"t")')
											f.write(';\n')
											inserted = True
											break
									if inserted:
										break
								if not inserted:
									self.ids['cc_alls'] += 1
									position += 1
									f.write('INSERT INTO cc_alls (id, construct_type, construct_id, created_at, updated_at, parent_id, position, ifbranch) VALUES ')
									f.write('(' + str(self.ids['cc_alls'])  + ',"CcQuestion",' + str(question.sqlID) + ',"' + str(question.created_at) + '","' + str(question.updated_at) + '",' + str(varGrp_val.cc_all_ID) + ',' + str(position) + ',"f")')
									f.write(';\n')
									break
						for statement in self.statement_constructs:
							if 's_q' + memberVariable == statement.textid:
								self.ids['cc_alls'] += 1
								position += 1
								f.write('INSERT INTO cc_alls (id, construct_type, construct_id, created_at, updated_at, parent_id, position, ifbranch) VALUES ')
								if inserted:
									f.write('(' + str(self.ids['cc_alls'])  + ',"CcStatement",' + str(statement.sqlID) + ',"' + str(statement.created_at) + '","' + str(statement.updated_at) + '",' + str(ifthenelse.getInstance(varGrp_val.cc_all_ID).cc_all_id) + ',' + str(ifthenelse.getInstance(varGrp_val.cc_all_ID).position) + ',"t")')
								else:
									f.write('(' + str(self.ids['cc_alls'])  + ',"CcStatement",' + str(statement.sqlID) + ',"' + str(statement.created_at) + '","' + str(statement.updated_at) + '",' + str(varGrp_val.cc_all_ID) + ',' + str(position) + ',"f")')
								f.write(';\n')
								break
					varGrp_val.linked = True
