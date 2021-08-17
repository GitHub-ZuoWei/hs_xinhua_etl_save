# uncompyle6 version 3.5.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.5 (default, Apr 19 2019, 17:01:24) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: ../src\jsfw\JsfwXml.py
# Compiled at: 2019-03-20 12:53:14
u"""
Created on 2018年4月15日

@author: mes
"""
import uuid, time
from config import constantConfig as constConfig
from utils.FileUtil import FileUtil
import re, shutil, os

class JsfwXml(object):
    u"""
        简氏防务类数据类
    """

    def __init__(self):
        pass

    def get_namespace(self, element):
        u"""
                获取xml的命名空间
        """
        m = re.match('\\{.*\\}', element)
        if m:
            return m.group(0)
        return ''

    def parseXML(self, tree):
        u"""
                解析XML
        """
        self.__titlePath = '{0}title'
        self.__authorPath = '{0}authoredBy/{0}author/{0}authorName'
        self.__metadataPath = '{0}metadata'
        self.__countryPath = '{0}standardName'
        self.__contentPath = '{0}sect1'
        self.__p = re.compile('({.*})(.*)')
        self.__tags = '军事'
        self.__language = 'en'
        self.__title = None
        self.__author = None
        self.__country = None
        self.__dateTime = None
        self.__content = ''
        self.__img = None
        self.__localImgPath = None
        self.__newsId = str(uuid.uuid1()).replace('-', '')
        self.__inTime = time.strftime('%Y-%m-%d %H:%M:%S')
        root = tree.getroot()
        namespace = self.get_namespace(root.tag)
        self.__title = tree.find(self.__titlePath.format(namespace)).text
        content_elements = tree.findall(self.__contentPath.format(namespace))
        for content_element in content_elements:
            for children in content_element:
                m = self.__p.match(children.tag)
                if m != None:
                    if m.group(2) == 'para':
                        for child in children:
                            self.__content += child.text

                        self.__content += children.text
                    elif m.group(2) == 'mediaBlock':
                        if children.getchildren()[0].attrib['imageType'] == 'picture':
                            self.__img = 'p' + children.getchildren()[0].attrib['vurl'] + '.jpg'
                        elif children.getchildren()[0].attrib['imageType'] == 'graphic':
                            self.__img = 'g' + children.getchildren()[0].attrib['vurl'] + '.jpg'

        metadata_element = tree.find(self.__metadataPath.format(namespace))
        date_flag = 0
        for children in metadata_element:
            m = self.__p.match(children.tag)
            if m != None:
                if m.group(2) == 'date':
                    date_flag += 1
                    if date_flag == 2:
                        dateTime = children.text
                        self.__dateTime = dateTime[:4] + '-' + dateTime[4:6] + '-' + dateTime[6:8] + ' 00:00:00'
                if m.group(2) == 'country':
                    country_namespace = m.group(1)
                    self.__country = children.find(self.__countryPath.format(country_namespace)).text

        if self.__dateTime is None:
            self.__dateTime = time.strftime('%Y-%m-%d %H:%M:%S')
        return

    @property
    def getImg(self):
        return self.__img

    def jsfwValid(self):
        u"""
                数据验证
        """
        if self.__title is None or self.__title == '':
            return False
        titleId = str(uuid.uuid5(uuid.NAMESPACE_DNS, self.__title.strip().encode('utf-8').lower())).replace('-', '')
        element = self.redis.insert(name=constConfig.redis_jsfw_titles, value=titleId, kind='set')
        if element == 0:
            return False
        else:
            return True

    def savePicOrFile(self, fileName, basePath, sTypePath):
        str_time = time.strftime('%Y%m%d')
        year_path = os.path.join(basePath, str_time[:4]).replace('\\', '/')
        time_path = os.path.join(year_path, str_time).replace('\\', '/')
        lastPath = os.path.join(time_path, sTypePath).replace('\\', '/')
        FileUtil.mkdir(year_path)
        FileUtil.mkdir(time_path)
        FileUtil.mkdir(lastPath)
        imgName = self.__newsId + '.jpg'
        webPath = os.path.join(('/').join(fileName.split('/')[:-1]), 'images', self.__img).replace('\\', '/')
        absolutePath = os.path.join(lastPath, imgName).replace('\\', '/')
        shutil.copyfile(webPath, absolutePath)
        self.__localImgPath = os.path.join('/temp', str_time[:4], str_time, sTypePath, imgName).replace('\\', '/')

    def getHsNewsValueTuple(self, *kw):
        u"""
                新闻详情表hs_news值
        """
        valueTuple = (
         self.__newsId, constConfig.const_one, self.__title, self.__dateTime,
         self.__content, self.__localImgPath, None, None,
         constConfig.const_zero, self.__inTime, None, None,
         self.__inTime, None, kw[0])
        return valueTuple

    def getHsNewsJorValueTuple(self, *kw):
        u"""
                新闻简表：hs_news_jor
        """
        countryType = self.sysconfig.countryNumByCountryEnDict.get(self.__country)
        sourceType = self.sysconfig.sourceDict.get(unicode(constConfig.jsfwName, 'utf-8'))
        self.__languageType = self.sysconfig.numByLanguageCodeDict.get(self.__language)
        self.__webFieldType = self.sysconfig.fieldTypeByRule(countryType, sourceType, None, self.__tags, None, self.__languageType, None, None, None, '%s %s' % (self.__title, self.__content))
        valueTuple = (
         self.__newsId, constConfig.const_one, self.__title, None,
         self.__webFieldType, None, countryType, self.__languageType,
         sourceType, self.__localImgPath, constConfig.const_one, self.__dateTime,
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