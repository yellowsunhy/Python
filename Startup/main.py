# This Python file uses the following encoding:utf-8
import sys
import re
import urllib
from bs4 import BeautifulSoup
config = "config"

def run():
	f = open(config,'r')
	lines = f.readlines()
	f = open(config,'w')
	for line in lines:
		strs = line.rstrip().rsplit(':')
		if strs[0] == "running":
			strs[1] = "1"
		f.write(strs[0]+":"+strs[1]+"\n")

def checkStop():
	f = open(config,'r')
	lines = f.readlines()
	for line in lines:
		strs = line.rstrip().rsplit(':')
		if strs[0] == "running" and strs[1] == "1":
			return 1
		elif strs[0] == "running" and strs[1] == "0":
			# print "The program is asked to stop!"
			return 0

# Get URL Contents
def getURLContents(url):
	if url == "" : return ""
	sock = urllib.urlopen(url)
	content = sock.read()
	return content

# Get Search Result
def getSearchResult(url):
	htmlSource = getURLContents(url)
	return getJobPreview(htmlSource)

# Get Job Preview
def getJobPreview(htmlSource):
	soup = BeautifulSoup(htmlSource)
	result = soup.find('div','resultListDiv')
	jobs = result.find_all("a","jobname")
	companies = result.find_all("a","coname")
	areas = result.find_all("td","td3")
	dates = result.find_all("td","td4")

	convertedJobs = []
	for i in range(0,len(jobs)):
		convertedJob = {}
		convertedJob['jobName'] = jobs[i].get_text()
		convertedJob['jobLink'] = jobs[i].get('href')
		convertedJob['companyName'] = companies[i].get_text()
		convertedJob['companyLink'] = companies[i].get('href')
		convertedJob['location'] = areas[i+1].get_text()
		convertedJob['date'] = dates[i+1].get_text()
		html = getURLContents(convertedJob['jobLink'])
		convertedJob = getJobDetail(html,convertedJob)
		print convertedJob['companyIndustry']
		convertedJobs.append(convertedJob)
	return convertedJobs

# Check Array
def checkArray(arr,i):
	if len(arr) == 0:
		return ""
	else:
		return arr[i]

# Get Job Detail
def getJobDetail(htmlSource,convertedJob):
	if htmlSource == "":	return convertedJob
	industry = re.findall(r"<strong>"+u"公司行业：".encode("gb2312")+"</strong>&nbsp;&nbsp;([^\<]*)",htmlSource)
	companyProperty = re.findall(r"<strong>"+u"公司性质：".encode("gb2312")+"</strong>&nbsp;&nbsp;([^\<]*)",htmlSource)	
	entryLevel = re.findall(r""+u"工作年限：".encode("gb2312")+"</td><td class=\"txt_2\">([^\<]*)",htmlSource)
	languageLevel = re.findall(r""+u"语言要求：".encode("gb2312")+"</td><td class=\"txt_2\">([^\<]*)",htmlSource)
	certificate = re.findall(r""+u"历：".encode("gb2312")+"</td><td class=\"txt_2\">([^\<]*)",htmlSource)
	jobFunction = re.findall(r"<strong>"+u"职位职能:".encode("gb2312")+"</strong>&nbsp;&nbsp;([^\<]*)",htmlSource)
	description = re.findall(r"<strong>"+u"职位描述:".encode("gb2312")+"</strong><br/>\n(.*)</td>",htmlSource)

	convertedJob['companyIndustry'] = checkArray(industry,0).decode("gb2312")
	convertedJob['companyProperty'] = checkArray(companyProperty,0).decode("gb2312")
	convertedJob['jobEntry'] = checkArray(entryLevel,0).decode("gb2312")
	convertedJob['jobLanguage'] = checkArray(languageLevel,0).decode("gb2312")
	convertedJob['jobCertificate'] = checkArray(certificate,0).decode("gb2312")
	convertedJob['jobFunction'] = checkArray(jobFunction,0).decode("gb2312")
	convertedJob['jobDescription'] = checkArray(description,0).decode("gb2312")
	return convertedJob

# Get Page Read
def getPageRead(page,keyword):
	page = str(page)
	url = "http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=000000%2C00&district=000000&funtype=0000&industrytype=00&issuedate=9&providesalary=99&keyword="+keyword+"&keywordtype=2&curr_page="+page+"&lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=01&lonlat=0%2C0&radius=-1&ord_field=0&list_type=0&fromType=14"
	jobs = getSearchResult(url)
	if len(jobs) == 0:
		print "Task Done!"
		return 0
	else:
		# print jobs
		return 1

# Save Job, Company to Database
# def saveToDatabase(jobs, companies):
# import MySQLdb as mdb
# import sys


run()
page = 1
while checkStop():
	taskResult = getPageRead(page,"海归")
	if taskResult == 0:
		page = 1
	else:
		page = page + 1


# f = open('search_detail.html','r')
# htmlSource = f.read()
# url = "http://search.51job.com/job/54065116,c.html"
# htmlSource = getURLContents(url)
# c = getJobDetail(htmlSource,{})
# print c["companyIndustry"]
# title find("td","sr_bt")
# company find("a","href like http://search.51job.com/list/")
# content find("div","jobs_com")[0]



# con = None
# con = mdb.connect('localhost', 'python_robot', '', 'db_MisterSun')
# with con:
# 	cur = con.cursor()
# 	cur.execute("SELECT * FROM album")
# 	cur.execute("INSERT INTO admin VALUES ('ADMIN','1')")
# 	rows = cur.fetchall()
# 	for row in rows:
# 		print row
