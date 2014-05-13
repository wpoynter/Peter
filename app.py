#!/usr/bin/python

import argparse
import os.path

from parser import Parser
from outputer import Outputer

def is_valid_file(arg_parser, arg):
	if not os.path.exists(arg):
		arg_parser.error('The file %s does not exist!"%arg')
	else:
		return open(arg,'r')    #return an open file handle


arg_parser = argparse.ArgumentParser(description='Parse and xml file from the data archive into a format suitable for loading into Caddies.')
arg_parser.add_argument('-i', dest='infilename', required=True, help='Input file to be parsed', metavar="FILE", type=lambda x: is_valid_file(arg_parser,x))
arg_parser.add_argument('-o', dest='outfilename', required=False, help='Output file', metavar="FILE", default="")
arg_parser.add_argument('--processes', dest='np', required=False, help='Number of processes to be used for the cleaning stage', type=int, default=4)
arg_parser.add_argument('--defaults', action='store_true', required=False, help='Use default values for every user decision (recommended for headless running)')
args = arg_parser.parse_args()

parser = Parser(args)

parser.run()

parser.output()

parser.clean()

parser.output()

parser.validate()

outputer = Outputer(parser.getData())

outputer.write('output.sql')
