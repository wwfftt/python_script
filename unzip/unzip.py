#!/usr/bin/env python
# coding=utf-8

import zipfile
import optparse
from threading import Thread

def ExtractFile(zFile,password):
	try:
		zFile.extractall(pwd=password)
		print '[+] Password : ' + password +'\n'
	except Exception as e:
		pass

def main():
	parser = optparse.OptionParser("usage %prog " + "-f <zipfile> -d <dictionary>")
	parser.add_option('-f', dest='fname', type='string', help='zip file')
	parser.add_option('-d', dest='dname', type='string', help='dictionary file')
	(options, args) = parser.parse_args()

	if (options.fname == None) | (options.dname == None):
		print parser.usage
		exit(0)
	else:
		fname = options.fname
		dname = options.dname

	zFile = zipfile.ZipFile(fname)
	passFile = open(dname)
	for line in passFile.readlines():
		password = line.strip('\n')
		t = Thread(target=ExtractFile,args=(zFile,password))
		t.start()

if __name__ == '__main__':
	main()