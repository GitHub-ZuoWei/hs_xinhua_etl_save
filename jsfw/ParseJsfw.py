# uncompyle6 version 3.5.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.5 (default, Apr 19 2019, 17:01:24) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: ../src\jsfw\ParseJsfw.py
# Compiled at: 2019-03-19 11:24:23
u"""
Created on 2018年4月15日

@author: mes
"""
import sys, os, requests, shutil, pysolr, redis, utils.Mod_logger as log, xml.etree.ElementTree as ET
from utils.RedisClient import RedisClient
from sysConfig.SysConfig import SysConfig
import config.Config
from jsfw.JsfwXml import JsfwXml
from utils.ZipUtil import ZipUtil
from utils.CommonUtil import CommonUtil
from config import constantConfig as constConfig
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

class ParseJsfw(JsfwXml):
    u"""
        简氏防务
        格式：
    """

    def __init__(self):
        self.hsNewsDataList = []
        self.hsNewsJorDataList = []
        self.solrLists = []
        self.hsNewsDataNums = 0

    def getIncrementData(self):
        u"""
                获取增量文件
        return:返回解压的文件夹路径
        """
        filenames = os.listdir(config.jsfwPath)
        for filename in filenames:
            if constConfig.jsfw_reges in filename:
                element = self.redis.insert(name=constConfig.redis_jsfw_zip, value=filename, kind='set')
                if element == 1:
                    extractFilePath = config.jsfwPath + '/' + filename
                    extractToFilePath = config.jsfwExtractFilePath + '/' + filename[:-4]
                    uipath = unicode(extractFilePath, 'utf-8')
                    zipUtil = ZipUtil(uipath)
                    zipUtil.extract_to(extractToFilePath)
                    zipUtil.close()
                    dataDirsPath = extractToFilePath + '/janesxml/data/news/jdw'
                    fileDirsPath = os.listdir(dataDirsPath)
                    for fileDirs in fileDirsPath:
                        fileNames = os.listdir(dataDirsPath + '/' + fileDirs)
                        for t_file in fileNames:
                            if t_file[-4:] == '.xml':
                                fileNamePath = (dataDirsPath + '/' + fileDirs + '/' + t_file).replace('\\', '/')
                                yield fileNamePath

                    shutil.rmtree(extractToFilePath)

    def parseFile(self):
        try:
            for fileName in self.getIncrementData():
                try:
                    tree = ET.parse(fileName)
                    self.parseXML(tree)
                    validResult = self.jsfwValid()
                    if validResult is False:
                        continue
                    try:
                        if self.getImg is not None:
                            self.savePicOrFile(fileName, config.localBasePath, constConfig.libPicPath['2'])
                    except Exception as e:
                        self.logger.exception(e)

                    hsNewsValueTuple = self.getHsNewsValueTuple(fileName)
                    hsNewsJorValueTuple = self.getHsNewsJorValueTuple()
                    solrTuple = self.getSolrValueTuple(hsNewsJorValueTuple)
                    solrDict = self.sysconfig.solrInfoDict(solrTuple)
                    self.hsNewsDataList.append(hsNewsValueTuple)
                    self.hsNewsJorDataList.append(hsNewsJorValueTuple)
                    self.solrLists.append(solrDict)
                    self.hsNewsDataNums = self.hsNewsDataNums + 1
                    if self.hsNewsDataNums >= int(config.jsfwInsertSqlPers):
                        self.lock.acquire()
                        self.insertSqlProcess()
                        self.lock.release()
                except Exception as e:
                    self.logger.exception(e)

            if self.hsNewsDataNums != 0:
                self.lock.acquire()
                self.insertSqlProcess()
                self.lock.release()
        except Exception as e:
            self.logger.exception(e)

        return

    def insertSqlProcess(self):
        u"""
                批量插入数据
        """
        maxValue = self.sysconfig.getDynamicTable('hs_news_')
        tableCodeDict = {}
        tableCodeDict['tableCode'] = int(maxValue)
        self.sysconfig._cursor.executemany('INSERT INTO hs_news_' + maxValue + constConfig.hsNewsSql, self.hsNewsDataList)
        self.sysconfig._cursor.executemany(constConfig.hsNewsJorSql, [ self.hsNewsJorDataList[i] + (maxValue,) for i in range(self.hsNewsDataNums) ])
        self.sysconfig._conn.commit()
        if config.isIndex == '1':
            self.solr.add([ CommonUtil.merge_two_dicts(self.solrLists[i], tableCodeDict) for i in range(self.hsNewsDataNums) ], commit=True)
        self.hsNewsDataNums = 0
        self.hsNewsDataList = []
        self.hsNewsJorDataList = []
        self.solrLists = []

    def jsfwProcess(self, lock):
        function_name = sys._getframe().f_code.co_name
        self.logger = log.init_log(config.logBasePath + '/' + function_name + '.log')
        self.logger.info('init ' + function_name)
        try:
            self.redis = RedisClient()
            self.redis.redis.ping()
            self.lock = lock
            self.sysconfig = SysConfig()
            solrCoreAdmin = pysolr.SolrCoreAdmin(self.sysconfig.solrIp)
            solrCoreAdmin.status()
            self.solr = pysolr.Solr(self.sysconfig.solrIp)
            self.parseFile()
            self.sysconfig.close()
        except requests.exceptions.ConnectionError as e:
            error_message = 'Failed to connect to solr server, are you sure that URL is correct? Checking it in a browser might help!'
            self.logger.error(error_message)
        except redis.exceptions.ConnectionError as e:
            self.logger.error(e)
        except Exception as e:
            self.logger.exception(e)


if __name__ == '__main__':
    pass