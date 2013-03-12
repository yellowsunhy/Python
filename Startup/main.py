# This Python file uses the following encoding:utf-8
import sys
import re
from bs4 import BeautifulSoup

from lib.config.config import *
from lib.parse.parser import *
from lib.db.db import *


# Get Page Read
def getPageRead(page,keyword):
	page = str(page)
	print "Page "+page

	url = "http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=000000%2C00&district=000000&funtype=0000&industrytype=00&issuedate=9&providesalary=99&keyword="+keyword+"&keywordtype=2&curr_page="+page+"&lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=01&lonlat=0%2C0&radius=-1&ord_field=0&list_type=0&fromType=14"
	print "Getting HTML Contents"
	htmlSource = getURLContents(url)

	print "Capturing Jobs"
	jobs = getJobs(htmlSource)

	print 'Saving Jobs'
	for job in jobs:
		saveJobs(job)

	if len(jobs) == 0:
		print "Task Finished!"
		return 0
	else:
		# print jobs
		return 1

# Save Job, Company to Database
# def saveToDatabase(jobs, companies):
# import MySQLdb as mdb
# import sys

# Run the main.py and config will be written to 1
run()
page = 1
while checkStop():
	taskResult = getPageRead(page,"海归")
	if taskResult == 0:
		page = 1
	else:
		page = page + 1
