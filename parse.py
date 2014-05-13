#!/usr/bin/python

import argparse
import os.path
import xml.etree.ElementTree as ET

from classes.category import Category

def is_valid_file(parser, arg):
	if not os.path.exists(arg):
		parser.error('The file %s does not exist!"%arg')
	else:
		return open(arg,'r')	#return an open file handle

def filter(input):
	return input.replace("{http://www.icpsr.umich.edu/DDI}", "")

def strip(input):
	return input.replace('\n','')

parser = argparse.ArgumentParser(description='Parse and xml file from the data archive into a format suitable for loading into Caddies.')
parser.add_argument('-i', dest='filename', required=True, help='Input file to be parsed', metavar="FILE", type=lambda x: is_valid_file(parser,x))
args = parser.parse_args()

tree = ET.parse(args.filename)
root = tree.getroot()
questions = []

for child in root:
	print filter(child.tag), child.attrib
	for gchild in child:
		if filter(gchild.tag) != 'var' : continue
		#print filter("\t" + gchild.tag), gchild.attrib
		#questions.append({})
		#questions[-1].attrib['ID'] = gchild.attrib['ID']
		#questions[-1].attrib['label'] = gchild.labl.text
		print '\033[91m' + filter(gchild.attrib['ID']) + '\033[0m'
		for ggchild in gchild:
			if filter(ggchild.tag) == 'labl':
				print '\033[95m\tLabel: \033[0m' + ggchild.text
			if filter(ggchild.tag) == 'universe':
                                print '\033[95m\tUniverse: \033[0m' + ggchild.text
			if filter(ggchild.tag) == 'qstn':
				for gggchild in ggchild:
					print '\033[95m\t' + filter(gggchild.tag) + ': \033[0m' + strip(gggchild.text)
			if filter(ggchild.tag) == 'valrng':
				for gggchild in ggchild:
					print '\033[95m\tRange\033[0m'
					print '\033[92m\t\tMax: ' + gggchild.attrib['max'] + '\033[0m'
					print '\033[92m\t\tMin: ' + gggchild.attrib['min'] + '\033[0m'
			if filter(ggchild.tag) == 'catgry':
                                for gggchild in ggchild:
					if filter(gggchild.tag) == 'labl':
                                        	print '\033[93m\t\t\t' + gggchild.text + '\033[0m'

print "Finished!";
