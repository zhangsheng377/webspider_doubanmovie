# coding:utf-8
import urllib2
from HTMLParser import HTMLParser
import sys
import time

reload(sys)
sys.setdefaultencoding('utf8')


def getHtml(url):
    try:
        user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36'
        headers = {'User-Agent': user_agent}
        request = urllib2.Request(url, headers=headers)
        page = urllib2.urlopen(request)
        html = page.read()
        return html
    except urllib2.URLError, e:
        if hasattr(e, "reason"):
            print u"豆瓣链接错误，错误原因", e.reason
            print url
        return ""


startid_file=open("startid.dat",'r')
start_s=startid_file.read()
startid=int(start_s)
startid_file.close()
for i in range(startid+1,9999999):
    id = str(i)

    myurl = 'https://api.douban.com/v2/movie/subject/'+id
    html = getHtml(myurl)
    print i, "\t", len(html)
    if len(html) > 200:
        file = open("output.dat", 'a+')
        file.write(html+"\n")
        file.close()
    startid_file = open("startid.dat", 'w')
    startid_file.write(str(i))
    startid_file.close()
    time.sleep(6)


