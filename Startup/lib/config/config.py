# This Python file uses the following encoding:utf-8

config_file = "lib/config/config"

def run():
	f = open(config_file,'r')
	lines = f.readlines()
	f = open(config_file,'w')
	for line in lines:
		strs = line.rstrip().rsplit(':')
		if strs[0] == "running":
			strs[1] = "1"
		f.write(strs[0]+":"+strs[1]+"\n")

def checkStop():
	f = open(config_file,'r')
	lines = f.readlines()
	for line in lines:
		strs = line.rstrip().rsplit(':')
		if strs[0] == "running" and strs[1] == "1":
			return 1
		elif strs[0] == "running" and strs[1] == "0":
			# print "The program is asked to stop!"
			return 0