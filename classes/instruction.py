#!/usr/bin/python
# -*- coding: utf-8 -*-

class Instruction(object):
    ID = 0
    def __init__(self, text):
        Instruction.ID += 1
        self.ID = Instruction.ID
        self.text = text
        self.uses = 1
