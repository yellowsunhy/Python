import pymongo
from pymongo import MongoClient

current_database = None
db_name = 'ChineseCareerEngine'
job_collection = 'JobCollection'

def connect():
	global db_name
	connection = MongoClient('localhost', 27017)
	database = connection[db_name]
	current_database = database
	return database

def getCollection(collection_name):
	global current_database
	if current_database == None:
		current_database = connect()
	collection = current_database[collection_name]
	return collection

def insert(col, el):
	collection = getCollection(col)
	el_id = collection.insert(el)
	return el_id

def update(col, query, value):
	collection = getCollection(col)
	collection.update(query, {
		'$set': value
	})

def select_one(col, query):
	collection = getCollection(col)
	result = collection.find_one(query)
	return result

def select_all(col, query):
	collection = getCollection(col)
	result = collection.find(query)
	return result

def saveJobs(convertedJob):
	job = {}
	try:
		job = {
			"JobName": convertedJob['jobName'],
			"JobLink": convertedJob['jobLink'],
			"JobLocation": convertedJob['location'],
			"JobEntry": convertedJob['jobEntry'],
			"JobLanguage": convertedJob['jobLanguage'],
			"JobCertificate": convertedJob['jobCertificate'],
			"JobFunction": convertedJob['jobFunction'],
			"JobDescription": convertedJob['jobDescription'],

			"CompanyName": convertedJob['companyName'],
			"CompanyLink": convertedJob['companyLink'],
			"CompanyIndustry": convertedJob['companyIndustry'],
			"CompanyProperty": convertedJob['companyProperty'],

			"PostDate": convertedJob['date']
		}
	except Exception, e:
		print "Something wrong with the database!"
	finally:
		global job_collection
		maybeExisted = select_one(job_collection,{
			"JobName": job["JobName"],
			"JobDescription": job['JobDescription'],
			"CompanyName": job["CompanyName"],
			"PostDate": job["PostDate"]
		})
		if maybeExisted == None:
			insert(job_collection, job)
			print "Insert " + job["JobName"]
		else:
			update(job_collection, maybeExisted, job)
			print "Update " + job["JobName"]


if __name__ == "__main__":
	# posts = [{
	# 	"author": "Sun",
	# 	"text": "My first blog post!!"
	# },
	# {
	# 	"author": "Sun",
	# 	"text": "My Second blog post!!"
	# }]
	# print insert('posts',posts)
	results = select_all(job_collection,{})
	for result in results:
		print result
	# print select_one('posts',{'author': 'Sun2'})
	# print select_all(job_collection,{})







