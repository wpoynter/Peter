#!/usr/bin/python

def removeLineBreaks(string):
	return string.replace('\n','')

def ifYes(response,default):
	if len(response) == 0:
		compare = default
	else:
		compare = response
	return compare == "y" or compare == "Y" or compare.lower() == "yes"
