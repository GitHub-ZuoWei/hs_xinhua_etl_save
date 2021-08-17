# uncompyle6 version 3.5.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.5 (default, Apr 19 2019, 17:01:24) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: ../src\txs\TxsXml.py
# Compiled at: 2019-03-20 14:59:11
u"""
Created on 2018年4月15日

@author: mes
"""
from config import constantConfig as constConfig
import re, uuid, time, requests, sys
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

class TxsXml(object):
    u"""
        新华社四类数据类
    """

    def __init__(self):
        pass

    def get_namespace(self, element):
        u"""
                获取xml的命名空间
        """
        m = re.match('\\{.*\\}', element.tag)
        if m:
            return m.group(0)
        return ''

    def parseXML(self, tree):
        u"""
                解析XML
        """
        self.__sourceFromPath = '{0}Envelop/{0}SentFrom/{0}NameTopic/{0}Name'
        self.__titlePath = '{0}Items/{0}Item/{0}MetaInfo/{0}DescriptionMetaGroup/{0}Titles/{0}HeadLine'
        self.__dateTimePath = '{0}Items/{0}Item/{0}MetaInfo/{0}AdministrationMetaGroup/{0}CurrentRevisionTime'
        self.__contentPath = '{0}Items/{0}Item/{0}Contents/{0}ContentItem/{0}DataContent'
        self.__subjectClassPath = '{0}Items/{0}Item/{0}MetaInfo/{0}DescriptionMetaGroup/{0}SubjectCodes/{0}SubjectCode'
        self.__languagePath = '{0}Items/{0}Item/{0}MetaInfo/{0}DescriptionMetaGroup/{0}Language'
        self.__webFieldDict = {}
        self.__txs_p = re.compile(('^\\（(.*?)\\）(.*)').decode('utf-8'))
        self.__countryDict = {}
        self.__languageDict = {}
        self.__sourceFrom = None
        self.__title = None
        self.__titleWithOutField = None
        self.__titleField = None
        self.__dateTime = None
        self.__content = None
        self.__webCountryType = None
        self.__webCountry = None
        self.__areaType = None
        self.__NewsCategory = None
        self.__language = None
        self.__languageType = None
        self.__webFieldType = None
        self.__img = None
        self.__localImgPath = None
        self.__attributeJson = None
        self.__url = None
        self.__newsId = str(uuid.uuid1()).replace('-', '')
        self.__inTime = time.strftime('%Y-%m-%d %H:%M:%S')
        namespace = self.get_namespace(tree.getroot())
        self.__sourceFrom = tree.find(self.__sourceFromPath.format(namespace)).text
        self.__title = tree.find(self.__titlePath.format(namespace)).text
        self.__titleWithOutField = self.__title.strip()
        m = self.__txs_p.match(self.__titleWithOutField)
        if m != None:
            self.__titleField = m.group(1).encode('utf-8').replace(' ', '').split('·')[0].split('•')[0]
            self.__titleWithOutField = m.group(2)
        languageElement = tree.find(self.__languagePath.format(namespace))
        self.__language = languageElement.attrib['topicRef']
        dateTimeElement = tree.find(self.__dateTimePath.format(namespace))
        if dateTimeElement != None:
            self.__dateTime = dateTimeElement.text.replace('T', ' ')[:-6]
        if self.__dateTime is None:
            self.__dateTime = time.strftime('%Y-%m-%d %H:%M:%S')
        contentElement = tree.find(self.__contentPath.format(namespace))
        if contentElement != None:
            self.__content = contentElement.text
        subjectNode = tree.findall(self.__subjectClassPath.format(namespace))
        for subject in subjectNode:
            if subject.attrib['kind'] == 'XH_Internalinternational':
                international = subject.getchildren()[0].getchildren()[0].text
                self.__webCountry = self.__countryDict.get(international.strip().encode('utf-8'))

        return

    def txsValid(self):
        u"""
                数据验证
        """
        if self.__titleWithOutField is None:
            return False
        else:
            if self.__titleWithOutField.strip() == '':
                return False
            titleId = str(uuid.uuid5(uuid.NAMESPACE_DNS, self.__titleWithOutField.strip().encode('utf8').lower())).replace('-', '')
            element = self.redis.insert(name=constConfig.redis_txs_titles, value=titleId, kind='set')
            if element == 0:
                return False
            return True

    def insertSpiderTxsTags(self):
        u"""
                存储标题标签（当做分类）
                将标签插入表spider_txs_tags
        """
        if self.__titleField != None and self.__titleField != '':
            element = self.redis.insert(name=constConfig.redis_txs_titleField, value=self.__titleField, kind='set')
            if element == 1:
                newsId = str(uuid.uuid1()).replace('-', '')
                inTime = time.strftime('%Y-%m-%d %H:%M:%S')
                valueTuple = (newsId, self.__titleField, inTime)
                return valueTuple
        return

    def getHsNewsValueTuple(self, *kw):
        u"""
                新闻详情表hs_news值
        """
        sentiScore = None
        if self.__languageType == '38' and self.__content != None:
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
         self.__newsId, constConfig.const_one, self.__titleWithOutField, self.__dateTime,
         self.__content, self.__localImgPath, self.__attributeJson, self.__url,
         constConfig.const_zero, self.__inTime, None, None,
         self.__inTime, sentiScore, kw[0])
        return valueTuple

    def getHsNewsJorValueTuple(self, *kw):
        u"""
                新闻简表：hs_news_jor
        """
        sourceType = self.sysconfig.sourceDict.get(self.__sourceFrom)
        self.__languageType = self.sysconfig.numByLanguageCodeDict.get(self.__languageDict.get(self.__language))
        self.__webCountryType = self.sysconfig.countryNumByCountryDict.get(self.__webCountry)
        if self.__content != None and '目录' not in self.__titleWithOutField:
            if self.__languageType == '38':
                r = requests.post(constConfig.chineseNewsClassifyUrl, data={})
                label = r.text.split(' ')[0]
                prob = r.text.split(' ')[1]
                if float(prob) > 0.4 and label in constConfig.classifyLabels:
                    self.__webFieldType = self.sysconfig.fieldTypeByRule(self.__webCountryType, sourceType, None, self.__titleField, None, self.__languageType, None, None, None, '%s %s' % (self.__titleWithOutField, self.__content))
            else:
                self.__webFieldType = self.sysconfig.fieldTypeByRule(self.__webCountryType, sourceType, None, self.__titleField, None, self.__languageType, None, None, None, '%s %s' % (self.__titleWithOutField, self.__content))
        valueTuple = (
         self.__newsId, constConfig.const_one, self.__titleWithOutField, None,
         self.__webFieldType, None, self.__webCountryType, self.__languageType,
         sourceType, None, constConfig.const_one, self.__dateTime,
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