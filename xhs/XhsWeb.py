# uncompyle6 version 3.5.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.5 (default, Apr 19 2019, 17:01:24) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: ../src\xhs\XhsWeb.py
# Compiled at: 2019-03-29 16:20:13
u"""
Created on 2018年4月15日

@author: mes
"""
import uuid, time
from config import constantConfig as constConfig
from lxml import etree
import re, requests

class XhsWeb(object):
    u"""
        新华社数据类（爬取网页解析）
    """

    def __init__(self):
        pass

    def pageInfo(self, url):
        u"""
                获取跳转后的url,总页数
                输入url，会跳转到另一个页面才能获取总页数
        """
        self.__hqbzXpath = '//table[@id="TitleListTable"]'
        self.__hqbzContentPath = '//td[@class="mid04"]'
        self.__pagePath = '//div[@id="pageinfo"]'
        self.__language = 'zh'
        self.__pageReExp = re.compile('^总共(.*?)页.*')
        self.__redirectUrl = None
        self.__pages = None
        self.result = requests.Session()
        res = self.result.get(url, allow_redirects=False)
        self.__redirectUrl = res.headers['location']
        self.__urlIp = ('/').join(self.__redirectUrl.split('/')[0:3])
        res = self.result.get(self.__redirectUrl, allow_redirects=True)
        if res.status_code == 200:
            htmlhandle = res.text
            tree = etree.HTML(htmlhandle)
            pageElement = tree.xpath(self.__pagePath)
            pageinfo = pageElement[0].text.encode('utf-8')
            m = self.__pageReExp.match(pageinfo)
            if m != None:
                self.__pages = m.group(1).encode('utf-8').strip()
        return self.__pages

    @property
    def getRedirectUrl(self):
        return self.__redirectUrl

    @property
    def getHqbzXpath(self):
        return self.__hqbzXpath

    @property
    def getNewsTime(self):
        return self.__newsTime

    @property
    def getNewsTimeOfDateTime(self):
        return self.__newsTimeOfDateTime

    def parseHtml(self, link):
        u"""
                解析html
        """
        self.__title = None
        self.__country = None
        self.__newsTime = None
        self.__content = ''
        self.__webFieldType = None
        self.__img = None
        self.__localImgPath = None
        self.__newsId = str(uuid.uuid1()).replace('-', '')
        self.__inTime = time.strftime('%Y-%m-%d %H:%M:%S')
        titleElement = link.getchildren()[1].getchildren()[0].getchildren()[0]
        self.__title = titleElement.getchildren()[0].text.strip().encode('utf-8').decode('utf-8')
        newsTime = link.getchildren()[1].getchildren()[0].getchildren()[1].text.encode('utf-8').strip()
        self.__newsTimeOfDateTime = newsTime.replace('/', '-')
        self.__newsTime = self.__newsTimeOfDateTime + ' 00:00:00'
        titleUrl = self.__urlIp + titleElement.attrib['href']
        res = self.result.get(titleUrl, allow_redirects=True)
        if res.status_code == 200:
            contentHtmlhandle = res.text
            contentTree = etree.HTML(contentHtmlhandle)
            contentlinks = contentTree.xpath(self.__hqbzContentPath)[0]
            for contentlink in contentlinks:
                content = contentlink.tail
                if content != None:
                    self.__content += content.encode('utf8').strip()
                elif self.__content != '':
                    self.__content += '<br>'
                    self.__content += '<br>'

        self.__content = self.__content.decode('utf-8')
        return

    @property
    def getTitle(self):
        return self.__title

    def getHsNewsValueTuple(self, *kw):
        u"""
                新闻详情表hs_news值
        """
        sentiScore = None
        r = requests.post(constConfig.chineseSentimentAnalysisUrl, data={})
        negProb = r.text.split(' ')[0]
        posProb = r.text.split(' ')[1]
        if float(negProb) > 0.6:
            sentiScore = -1
        elif float(posProb) > 0.6:
            sentiScore = 1
        else:
            sentiScore = 0
        valueTuple = (
         self.__newsId, constConfig.const_one, self.__title, self.__newsTime,
         self.__content, None, None, None,
         constConfig.const_zero, self.__inTime, None, None,
         self.__inTime, sentiScore, None)
        return valueTuple

    def getHsNewsJorValueTuple(self, *kw):
        u"""
                新闻简表：hs_news_jor
        """
        fieldType = kw[0]
        sourceType = self.sysconfig.sourceDict.get(unicode(constConfig.xhsName, 'utf-8'))
        self.__languageType = self.sysconfig.numByLanguageCodeDict.get(self.__language)
        valueTuple = (self.__newsId, constConfig.const_one, self.__title, None,
         fieldType, None, None, self.__languageType,
         sourceType, self.__localImgPath, constConfig.const_one, self.__newsTime,
         self.__inTime, self.__inTime)
        return valueTuple

    def getSolrValueTuple(self, valueTuple):
        u"""
                索引值
        """
        contentTuple = (
         self.__content, None)
        return contentTuple + valueTuple


if __name__ == '__main__':
    pass