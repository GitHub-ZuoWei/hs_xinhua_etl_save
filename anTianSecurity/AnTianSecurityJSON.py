# uncompyle6 version 3.5.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.5 (default, Apr 19 2019, 17:01:24) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: ../src\anTianSecurity\AnTianSecurityJSON.py
# Compiled at: 2019-03-06 11:17:48
u"""
Created on 2018年4月15日

@author: mes
"""
import uuid, time, os, sys, requests
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from utils.TimeUtil import TimeUtil
from datetime import datetime
from config import constantConfig as constConfig

class AnTianSecurityJSON(object):
    u"""
        安天网络安全数据
        格式：Json格式
    """

    def __init__(self):
        pass

    def parseJson(self, dataDict):
        u"""
                解析json
        """
        self.__newsId = str(uuid.uuid1()).replace('-', '')
        self.__sourceType = dataDict.get('source')
        self.__type = dataDict.get('type')
        self.__title_cn = dataDict.get('title_cn')
        self.__keywords_cn = dataDict.get('keywords_cn')
        self.__content = dataDict.get('content').decode('utf-8', 'ignore')
        self.__languageCode = dataDict.get('languageCode')
        self.__fieldCode = dataDict.get('fieldCode')
        self.__linkUrl = dataDict.get('linkUrl')
        self.__countryCode = dataDict.get('countryCode')
        self.__newsTime = dataDict.get('newsTime')
        self.__creationTime = dataDict.get('creationTime')
        self.__inTime = time.strftime('%Y-%m-%d %H:%M:%S')

    def dataValid(self):
        u"""
                数据验证
        """
        newsTimeOfDateTime = datetime.strptime(self.__newsTime, '%Y-%m-%d %H:%M:%S')
        nowTimeOfDataTime = datetime.strptime(time.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        if TimeUtil.isVaildDate(self.__newsTime) == False:
            return False
        else:
            if TimeUtil.isVaildDate(self.__creationTime) == False:
                return False
            if self.__title_cn == None:
                return False
            if newsTimeOfDateTime > nowTimeOfDataTime:
                return False
            titleId = str(uuid.uuid5(uuid.NAMESPACE_DNS, self.__title_cn.lower())).replace('-', '')
            element = self.redis.insert(name=constConfig.redis_anTianSecurity_titles, value=titleId, kind='set')
            if element == 0:
                return False
            return True

    def getHsNewsValueTuple(self, *kw):
        u"""
                新闻详情表hs_news值
        """
        sentiScore = None
        if self.__languageCode == '38':
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
         self.__newsId, constConfig.const_one, self.__title_cn.decode('utf-8', 'ignore'), self.__newsTime,
         self.__content, None, None, self.__linkUrl,
         constConfig.const_zero, self.__creationTime, None, None,
         self.__inTime, sentiScore, kw[0])
        return valueTuple

    def getHsNewsJorValueTuple(self, *kw):
        u"""
                新闻简表：hs_news_jor
        """
        valueTuple = (
         self.__newsId, constConfig.const_one, self.__title_cn.decode('utf-8', 'ignore'), None,
         self.__fieldCode, None, self.__countryCode, self.__languageCode,
         self.__sourceType, None, constConfig.const_one, self.__newsTime,
         self.__creationTime, self.__inTime)
        return valueTuple

    def getSolrValueTuple(self, *kw):
        u"""
                索引值
        """
        valueTuple = kw[0]
        contentTuple = (self.__content, None)
        return contentTuple + valueTuple


if __name__ == '__main__':
    pass