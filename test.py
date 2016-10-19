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


class MyHTMLParser(HTMLParser):
    def _init_(self, id):
        self.title = ""
        self.isTitleTag = False
        self.title_Tag = "span"
        self.title_attr = [('property', 'v:itemreviewed')]

        self.year = 0
        self.isYearTag = False
        self.year_Tag = "span"
        self.year_attr = [('class', 'year')]

        self.count_briefComment = 0
        self.isBriefCommentTag = False
        self.briefComment_Tag = "a"
        self.briefComment_attr = [('href', 'https://movie.douban.com/subject/' + id + '/comments')]

        self.count_question = 0
        self.isQuestionTag = False
        self.question_Tag = "a"
        self.question_attr = [('href', 'https://movie.douban.com/subject/' + id + '/questions/?from=subject')]

        self.count_movieComment = 0
        self.isMovieCommentTag = False
        self.movieComment_Tag = "a"
        self.movieComment_attr = [('href', 'https://movie.douban.com/subject/' + id + '/reviews')]

        self.count_totalComment = 0

    def handle_starttag(self, tag, attr):
        if tag == self.title_Tag:
            if attr == self.title_attr:
                self.isTitleTag = True
                pass
        if tag == self.year_Tag:
            if attr == self.year_attr:
                self.isYearTag = True
                pass
        if tag == self.briefComment_Tag:
            if attr == self.briefComment_attr:
                self.isBriefCommentTag = True
                pass
        if tag == self.question_Tag:
            if attr == self.question_attr:
                self.isQuestionTag = True
                pass
        if tag == self.movieComment_Tag:
            if attr == self.movieComment_attr:
                self.isMovieCommentTag = True
                pass

    def handle_data(self, data):
        if self.isTitleTag == True:
            self.title = data.decode("utf-8").encode("gb18030")
            self.isTitleTag = False
        elif self.isYearTag == True:
            self.year = int(data[1:-1])
            self.isYearTag = False
        elif self.isBriefCommentTag == True:
            self.count_briefComment = int(filter(str.isdigit, data))
            self.isBriefCommentTag = False
        elif self.isQuestionTag == True:
            self.count_question = int(filter(str.isdigit, data))
            self.isQuestionTag = False
        elif self.isMovieCommentTag == True:
            self.count_movieComment = int(filter(str.isdigit, data))
            self.isMovieCommentTag = False

    def _count_totalComment(self):
        self.count_totalComment = self.count_briefComment + self.count_question + self.count_movieComment
        return self.count_totalComment


#file = open("output.dat", 'w')
parser = MyHTMLParser()
startid_file=open("startid.dat",'r')
start_s=startid_file.read()
startid=int(start_s)
startid_file.close()
for i in range(startid+1,9999999):
#for i in range(5045678, 5045679):
    # print i
    id = str(i)

    myurl = 'https://movie.douban.com/subject/' + id
    html = getHtml(myurl)
    print i, "\t", len(html)
    if len(html) > 40000:
        parser._init_(id)
        parser.feed(html)
        #if parser._count_totalComment() > 90000:
        print parser.title, "(", parser.year, ")"
        print "count_briefComment = ", parser.count_briefComment
        print "count_question = ", parser.count_question
        print "count_movieComment = ", parser.count_movieComment
        print "count_totalComment = ", parser.count_totalComment
        print ""
        file = open("output.dat", 'a+')
        file.write(parser.title + " " + str(parser.year) + " " + str(parser.count_briefComment) + " " + str(
                parser.count_question) + " " + str(parser.count_movieComment) + " " + str(
                parser.count_totalComment) + " " + myurl+"\n")
        file.close()
    startid_file = open("startid.dat", 'w')
    startid_file.write(str(i))
    startid_file.close()
    time.sleep(6)

parser.close()
file.close()
