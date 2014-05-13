#!/usr/bin/python

from multiprocessing import Pool

def f(x):
	return x**x

pool = Pool(processes=4)
print pool.map(f, range(10))
