# coding:utf-8
import urllib2
import time



def get_html(url):
    try:
        user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36'
        headers = {'User-Agent': user_agent}
        request = urllib2.Request(url, headers=headers)
        page = urllib2.urlopen(request)
        my_html = page.read()
        return my_html
    except urllib2.URLError, e:
        if hasattr(e, "reason"):
            print u"豆瓣链接错误，错误原因", e.reason
            print url
            if e.reason=="Bad Request":
                print "wait for reget_html......"
                waitsecond_file=open("waitsecond.dat", 'r')
                waitsecond=int(waitsecond_file.read())
                waitsecond_file.close()
                waitsecond_file = open("waitsecond.dat", 'w')
                waitsecond_file.write(str(waitsecond+1))
                waitsecond_file.close()
                time.sleep(60*60*2)
                return get_html(url)
        return ""


startId_file=open("startid.dat", 'r')
start_s=startId_file.read()
startId=int(start_s)
startId_file.close()
for i in range(startId+1,9999999):
    myId = str(i)

    myUrl = 'https://api.douban.com/v2/movie/subject/' + myId
    html = get_html(myUrl)
    print i, "\t", len(html)
    if len(html) > 200:
        my_file = open("output.dat", 'a+')
        my_file.write(html + "\n")
        my_file.close()
    startId_file = open("startid.dat", 'w')
    startId_file.write(str(i))
    startId_file.close()
    waitsecond_file=open("waitsecond.dat", 'r')
    waitsecond=int(waitsecond_file.read())
    waitsecond_file.close()
    time.sleep(waitsecond)


