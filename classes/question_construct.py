#!/usr/bin/python

import datetime

class QuestionConstruct(object):
	ID = 0
        def __init__(self, varid, textid question_item_id, response_unit_id):
		QuestionConstruct.ID += 1
		self.ID = QuestionConstruct.ID
                self.varid = varid
                self.textid = 'qc_' + textid
		self.parentless = True
		self.created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
		self.updated_at = self.created_at
