# uncompyle6 version 3.5.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.5 (default, Apr 19 2019, 17:01:24) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: ../src\internet\InterNetJSON.py
# Compiled at: 2019-03-29 18:42:31
u"""
Created on 2018年4月15日

@author: mes
"""
import uuid, time, langid, shutil, json, os, config.Config
from utils.RedisClient import RedisClient
from sysConfig.SysConfig import SysConfig
from utils.langconv import Converter
from utils.FileUtil import FileUtil
from utils.TimeUtil import TimeUtil
from datetime import datetime
from config import constantConfig as constConfig
import requests


class InterNetJSON(object):
    u"""
    互联网数据（包括新闻数据、工具数据（天气、汇率等））
    格式：Json格式
    """

    def __init__(self):
        self.sysconfig = SysConfig()
        self.redis = RedisClient()
        pass

    def parseJson(self, *kw):
        u"""
                解析json
        """
        fileName = kw[0]
        dataDict = kw[1]
        self.__publicDateTime = None
        self.__img = None
        self.__localImgPath = None
        self.__attributeJson = None
        self.__internetFieldType = None
        self.seg_text = []
        self.__fileLists = []
        self.__newsId = str(uuid.uuid1()).replace('-', '')
        self.__inTime = time.strftime('%Y-%m-%d %H:%M:%S')
        self.__siteCofName = dataDict.get('siteCofName')
        self.__siteCofId = dataDict.get('siteCofId')
        self.__title = dataDict.get('title')
        self.__titleTranslation = dataDict.get('titleTranslation')
        self.__contentShow = dataDict.get('contentShow')
        self.__contentForExport = dataDict.get('contentForExport')
        self.__contentTranslation = dataDict.get('contentTranslation')
        self.__region = dataDict.get('region')
        self.__url = dataDict.get('url')
        self.__guid = dataDict.get('guid')
        self.__creationTime = dataDict.get('creationTime')
        dataTime = dataDict.get('publicDateTime')
        if dataTime != None and dataTime != '':
            if len(dataTime.strip()) == 19:
                self.__publicDateTime = dataTime
            elif len(dataTime.strip()) == 10:
                self.__publicDateTime = dataTime.strip() + ' 00:00:00'
        else:
            self.__publicDateTime = dataDict.get('creationTime')
        excavateDataFileList = dataDict.get('excavateDataFileList')
        if excavateDataFileList != None:
            if len(excavateDataFileList) != 0:
                for fileDict in excavateDataFileList:
                    if fileDict['fileName'].split('.')[1] == 'pdf':
                        self.__fileLists.append(fileDict['fileName'])
                    elif fileDict['fileName'].split('.')[1] == 'jpg':
                        self.__img = fileDict.get('fileName')

        try:
            if self.__img != None:
                self.savePicOrFile(fileName, config.Config.localBasePath, constConfig.libPicPath['1'])
        except Exception as e:
            self.logger.exception(e)
        else:
            try:
                if len(self.__fileLists) != 0:
                    self.savePicOrFile(fileName, config.Config.localBasePath, constConfig.libFilePath['1'])
            except Exception as e:
                self.logger.exception(e)

        return

    @property
    def getSiteCofName(self):
        return self.__siteCofName

    def internetValid(self):
        u"""
                数据验证
        """
        newsTimeOfDateTime = datetime.strptime(self.__publicDateTime, '%Y-%m-%d %H:%M:%S')
        nowTimeOfDataTime = datetime.strptime(time.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        if TimeUtil.isVaildDate(self.__publicDateTime) == False:
            return False
        else:
            if TimeUtil.isVaildDate(self.__creationTime) == False:
                return False
            if self.__title == None or self.__title == '' or self.__title[-4:].lower() == '.jpg' or self.__title[
                                                                                                    -5:].lower() == '.jpeg' or self.__title[
                                                                                                                               -4:].lower() == '.pdf':
                return False
            if newsTimeOfDateTime > nowTimeOfDataTime:
                return False
            titleId = str(uuid.uuid5(uuid.NAMESPACE_DNS, self.__title.lower())).replace('-', '')
            element = self.redis.insert(name=constConfig.redis_internet_titles, value=titleId, kind='set')
            if element == 0:
                return False
            return True

    def savePicOrFile(self, *kw):
        fileName = kw[0]
        basePath = kw[1]
        sTypePath = kw[2]
        str_time = time.strftime('%Y%m%d')
        year_path = os.path.join(basePath, str_time[:4]).replace('\\', '/')
        time_path = os.path.join(year_path, str_time).replace('\\', '/')
        lastPath = os.path.join(time_path, sTypePath).replace('\\', '/')
        FileUtil.mkdir(year_path)
        FileUtil.mkdir(time_path)
        FileUtil.mkdir(lastPath)
        if self.__img is not None:
            imgName = self.__newsId + '.jpg'
            webPath = os.path.join(('/').join(fileName.split('/')[:-1]), self.__img).replace('\\', '/')
            absolutePath = os.path.join(lastPath, imgName).replace('\\', '/')
            shutil.copyfile(webPath, absolutePath)
            self.__localImgPath = os.path.join('/temp', str_time[:4], str_time, sTypePath, imgName).replace('\\', '/')
        if len(self.__fileLists) != 0:
            attrLists = []
            for pdfFile in self.__fileLists:
                try:
                    pdfName = str(uuid.uuid1()).replace('-', '') + '.pdf'
                    webPath = os.path.join(('/').join(fileName.split('/')[:-1]), pdfFile).replace('\\', '/')
                    absolutePath = os.path.join(lastPath, pdfName).replace('\\', '/')
                    localFilePath = os.path.join('/temp', str_time[:4], str_time, sTypePath, pdfName).replace('\\', '/')
                    shutil.copyfile(webPath, absolutePath)
                    attrDict = {}
                    attrDict['fileName'] = pdfFile
                    attrDict['filePath'] = localFilePath
                    attrLists.append(attrDict)
                except Exception as e:
                    pass

            if len(attrLists) != 0:
                self.__attributeJson = json.dumps(attrLists, encoding='utf-8', ensure_ascii=False)
        return

    def getHsNewsValueTuple(self, *kw):
        u"""
                新闻详情表hs_news值
        """
        sentiScore = None
        if len(self.__titleTranslation) != 0:
            r = requests.post(constConfig.chineseSentimentAnalysisUrl, data={})
            negProb = r.text.split(' ')[0]
            posProb = r.text.split(' ')[1]
            if float(negProb) > 0.6:
                sentiScore = -1
            elif float(posProb) > 0.6:
                sentiScore = 1
            else:
                sentiScore = 0
        elif self.languageType == '38':
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
            self.__newsId, constConfig.const_one, self.__title, self.__publicDateTime,
            self.__contentShow, self.__localImgPath, self.__attributeJson, self.__url,
            constConfig.const_zero, self.__creationTime, self.__titleTranslation, self.__contentTranslation,
            self.__inTime, sentiScore, kw[0])
        return valueTuple

    def getHsNewsJorValueTuple(self):
        u"""
                新闻简表：hs_news_jor
        """
        mediaSectionId = str(uuid.uuid5(uuid.NAMESPACE_DNS, self.__siteCofId)).replace('-', '')
        if mediaSectionId not in self.sysconfig.mediaSectionDict:
            mediaSectionId = self.sysconfig.mediaSectionIdByNameDict.get(self.__siteCofName.decode('utf-8'))
        mediaId = self.sysconfig.mediaByMediaSectionDict.get(mediaSectionId)
        countryNum = self.sysconfig.countryNumByMediaSectionDict.get(mediaSectionId)
        if mediaId != constConfig.weiXinMediaId:
            sourceType = self.sysconfig.sourceDict.get(unicode(constConfig.internetName, 'utf-8'))
        else:
            sourceType = self.sysconfig.sourceDict.get(unicode(constConfig.weiXinName, 'utf-8'))
        tags = self.sysconfig.tagsByMediaSectionDict.get(mediaSectionId)
        self.languageType = self.sysconfig.languageNumByMediaSectionDict.get(mediaSectionId)
        if self.languageType == None:
            languageCode = langid.classify(self.__contentShow)[0]
            self.languageType = self.sysconfig.numByLanguageCodeDict.get(languageCode)
        line = Converter('zh-hans').convert(self.__title.decode('utf-8', 'ignore'))
        if self.__title.decode('utf-8', 'ignore') != line:
            self.__titleTranslation = line
            self.__contentTranslation = Converter('zh-hans').convert(self.__contentShow.decode('utf-8', 'ignore'))
        if len(self.__titleTranslation) != 0:
            r = requests.post(constConfig.chineseNewsClassifyUrl, data={})
            label = r.text.split(' ')[0]
            prob = r.text.split(' ')[1]
            if float(prob) > 0.4 and label in constConfig.classifyLabels:
                self.__internetFieldType = self.sysconfig.fieldTypeByRule(countryNum, sourceType, mediaSectionId, tags,
                                                                          mediaId, self.languageType, None, None, None,
                                                                          '%s %s' % (self.__titleTranslation,
                                                                                     self.__contentTranslation))
        elif self.languageType == '38':
            r = requests.post(constConfig.chineseNewsClassifyUrl, data={})
            label = r.text.split(' ')[0]
            prob = r.text.split(' ')[1]
            if float(prob) > 0.4 and label in constConfig.classifyLabels:
                self.__internetFieldType = self.sysconfig.fieldTypeByRule(countryNum, sourceType, mediaSectionId, tags,
                                                                          mediaId, self.languageType, None, None, None,
                                                                          '%s %s' % (self.__title, self.__contentShow))
        else:
            self.__internetFieldType = self.sysconfig.fieldTypeByRule(countryNum, sourceType, mediaSectionId, tags,
                                                                      mediaId, self.languageType, None, None, None,
                                                                      '%s %s' % (self.__title, self.__contentForExport))
        valueTuple = (self.__newsId, constConfig.const_one, self.__title.decode('utf-8', 'ignore'), mediaSectionId,
                      self.__internetFieldType, None, countryNum, self.languageType,
                      sourceType, self.__localImgPath, constConfig.const_one, self.__publicDateTime,
                      self.__creationTime, self.__inTime)
        return valueTuple

    def getSolrValueTuple(self, *kw):
        u"""
                索引值
        """
        valueTuple = kw[0]
        contentTuple = (self.__contentShow.decode('utf-8', 'ignore'), self.__attributeJson)
        return contentTuple + valueTuple

    def getHsJoseonValueTuple(self, *kw):
        u"""
                朝鲜新闻分析主表hs_joseon表
        """
        sourceType = constConfig.Korea_sourceDict.get(kw[0], '1')
        valueTuple = (self.__newsId, self.__title, self.__publicDateTime, self.__contentShow,
                      sourceType, constConfig.const_zero, self.__inTime)
        return valueTuple

    def DataStatistics(self, *kw):
        u"""
                统计每个数据包的数量
        """
        fileDict = kw[0]
        fileList = []
        for fileName, counts in fileDict.iteritems():
            dataId = str(uuid.uuid5(uuid.NAMESPACE_DNS, fileName)).replace('-', '')
            oriTime = fileName[:19].replace('_', ':')
            inTime = time.strftime('%Y-%m-%d %H:%M:%S')
            valueTuple = (dataId, fileName, counts, oriTime,
                          inTime)
            fileList.append(valueTuple)

        self.sysconfig._cursor.executemany(constConfig.dataStatisticSql, fileList)
        self.sysconfig._conn.commit()


if __name__ == '__main__':
    l = '38'
    print l, type(l)
    if cmp(l, '38') == 0:
        print 'yes'
