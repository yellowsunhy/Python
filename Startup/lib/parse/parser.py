# This Python file uses the following encoding:utf-8
# 
from bs4 import BeautifulSoup
import re
import urllib

# Get URL Contents
def getURLContents(url):
    if url == "" : return ""
    sock = urllib.urlopen(url)
    content = sock.read()
    return content

# Get Job Preview and Detail
def getJobs(htmlSource):
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

        # print convertedJob['companyIndustry']
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
    if htmlSource == "":    return convertedJob
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

if __name__ == "__main__":
    f = open("../../test/search_detail.html",'r')
    # f = open("../../test/search_result.html",'r')

    # f = open("../../search_page.html",'r')
    # f = open("../../login_page.html",'r')

    html = f.read()
    print getSearchDetail(html)
    # form = setFormValue(html,{})
    # keylist = form.keys()
    # keylist.sort()
    # for key in keylist:
    #     print "%s:%s" % (key,form[key])



