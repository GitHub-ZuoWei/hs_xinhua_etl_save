# uncompyle6 version 3.5.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.5 (default, Apr 19 2019, 17:01:24) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: ../src\xhs\ParseXhs.py
# Compiled at: 2019-03-19 11:25:42
u"""
Created on 2018年4月17日

@author: mes
"""
from lxml import etree
import config.Config, requests
from sysConfig.SysConfig import SysConfig
import utils.Mod_logger as log
from XhsWeb import XhsWeb
from utils.CommonUtil import CommonUtil
import sys, pysolr, redis
from datetime import datetime
from config import constantConfig as constConfig
from utils.TimeUtil import TimeUtil
from utils.RedisClient import RedisClient

class ParseXhs(XhsWeb):
    u"""
        新华社二级站解析
        爬取策略：每次爬取新闻后，将爬取最新的标题（爬取结束位置）存入redis，
                        下次爬取时判断是否爬取到前一个爬取的位置，若是，则结束。
    """

    def __init__(self):
        self.xpathStr = '/html/body/table[2]/tbody/tr/td[3]/table[3]/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr[2]/td/table/tbody/tr/td'
        self.picNewsStr = '/html/body/table[2]/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[1]/td/span'
        self.hsNewsDataList = []
        self.hsNewsJorDataList = []
        self.solrLists = []
        self.hsNewsDataNums = 0

    def parseFile(self, xhsName, url):
        u"""
        :param xhsName:新华社专供子栏目名称
        :param url:子栏目的url
        """
        self.logger.info(xhsName)
        self.logger.info(url)
        try:
            fieldType = self.sysconfig.fieldDict.get(xhsName)
            self.pages = self.pageInfo(url)
            xhs_title = self.redis.fetch(name=constConfig.redis_xhs_dict.get(xhsName))
            self.logger.info('断点处')
            self.logger.info(xhs_title)
            isSpider = 0
            for page in xrange(int(self.pages)):
                try:
                    xhsUrl = self.getRedirectUrl + '&pageno=' + str(page + 1)
                    self.logger.info(xhsUrl)
                    if isSpider == 1:
                        break
                    res = self.result.get(xhsUrl, allow_redirects=True)
                    if res.status_code == 200:
                        htmlhandle = res.text
                        tree = etree.HTML(htmlhandle)
                        links = tree.xpath(self.getHqbzXpath)[0].getchildren()
                        for i in xrange(2, len(links)):
                            try:
                                self.parseHtml(links[i])
                                if page == 0 and i == 2:
                                    self.firstTitle = self.getTitle
                                if TimeUtil.isVaildDate(self.getNewsTime) == False:
                                    continue
                                self.logger.info(self.getTitle)
                                if self.getTitle == xhs_title.decode('utf-8'):
                                    self.redis.insert(constConfig.redis_xhs_dict.get(xhsName), self.firstTitle.encode('utf-8'), kind='string')
                                    isSpider = 1
                                    break
                                hsNewsValueTuple = self.getHsNewsValueTuple()
                                hsNewsJorValueTuple = self.getHsNewsJorValueTuple(fieldType)
                                solrTuple = self.getSolrValueTuple(hsNewsJorValueTuple)
                                solrDict = self.sysconfig.solrInfoDict(solrTuple)
                                self.hsNewsDataList.append(hsNewsValueTuple)
                                self.hsNewsJorDataList.append(hsNewsJorValueTuple)
                                self.solrLists.append(solrDict)
                                self.hsNewsDataNums = self.hsNewsDataNums + 1
                                if self.hsNewsDataNums >= int(config.xhsInsertSqlPers):
                                    self.lock.acquire()
                                    self.insertSqlProcess()
                                    self.lock.release()
                            except Exception as e:
                                self.logger.exception(e)

                except Exception as e:
                    self.logger.exception(e)

            if self.hsNewsDataNums != 0:
                self.lock.acquire()
                self.insertSqlProcess()
                self.lock.release()
        except Exception as e:
            self.logger.exception(e)

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

    def xhsProcess(self, lock):
        function_name = sys._getframe().f_code.co_name
        self.logger = log.init_log(config.logBasePath + '/' + function_name + '.log')
        self.logger.info('init ' + function_name)
        try:
            self.redis = RedisClient()
            self.redis.redis.ping()
            self.sysconfig = SysConfig()
            xhsWebConfigDict = self.sysconfig.getXhsWebConfig()
            self.lock = lock
            solrCoreAdmin = pysolr.SolrCoreAdmin(self.sysconfig.solrIp)
            solrCoreAdmin.status()
            requests.get(constConfig.nlpUrl)
            self.solr = pysolr.Solr(self.sysconfig.solrIp)
            for xhsName, url in xhsWebConfigDict.iteritems():
                self.parseFile(xhsName, url)

        except requests.exceptions.ConnectionError as e:
            error_message = 'Failed to connect to solr server, are you sure that URL is correct? Checking it in a browser might help!\n                             or failed to connect NLP server!'
            self.logger.error(error_message)
        except redis.exceptions.ConnectionError as e:
            self.logger.error(e)
        except Exception as e:
            self.logger.exception(e)


if __name__ == '__main__':
    pass