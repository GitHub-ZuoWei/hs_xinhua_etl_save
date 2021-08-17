# uncompyle6 version 3.5.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.5 (default, Apr 19 2019, 17:01:24) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: ../src\zyfw\ZyfwJSON.py
# Compiled at: 2019-04-10 15:22:57
u"""
Created on 2018年4月15日

@author: mes
"""
import uuid, time, json, os, config.Config
from utils.FileUtil import FileUtil
from utils.ZipUtil import ZipUtil
from utils.CJsonEncoder import CJsonEncoder
from config import constantConfig as constConfig

class ZyfwJSON(object):
    u"""
        知远防务数据解析
        修改记录：
    20180531-1022 删除hs_zyfw_config中attr中summar属性，因为和introduction记录重复
    """

    def __init__(self):
        pass

    def getZyfwLibLists(self, *kw):
        u"""
                获取知远防务数据表名为dbId的数据
        SQL Server CONVERT() 函数:http://www.w3school.com.cn/sql/func_convert.asp
        """
        dbId = kw[0]
        lastCrawTime = kw[1]
        ZyfwLibSql = "select * from %s where ('%s' <= CONVERT(varchar, AddDate,20)) " % (dbId, lastCrawTime)
        self.sqlServerDB._cursor.execute(ZyfwLibSql)
        self.zyfwLists = self.sqlServerDB._cursor.fetchall()

    def updateZyfwCrawTime(self, *kw):
        u"""
                记录知远防务数据解析的时间
        """
        dbId = kw[0]
        crawTime = time.strftime('%Y-%m-%d %H:%M:%S')
        ZyfwConfigSql = "update hs_zyfw_config set lastCrawTime = '%s' where dbId= '%s'" % (crawTime, dbId)
        self.sysconfig._cursor.execute(ZyfwConfigSql)
        self.sysconfig._conn.commit()
        return crawTime

    def parseLibInfo(self, *kw):
        u"""
                解析每个数据库
        """
        zyfwConfigDict = kw[0]
        zyfwDict = kw[1]
        imgField = zyfwConfigDict.get('imgField')
        fileFields = zyfwConfigDict.get('fileField')
        imgList = []
        fileList = []
        self.savePicPath = None
        self.saveFilePath = None
        self.libraryId = str(uuid.uuid1()).replace('-', '')
        self.title = zyfwDict.get('Title')
        self.author = zyfwDict.get('Author')
        self.summary = zyfwDict.get('Summary')
        self.region = zyfwDict.get('Countries')
        self.oriTime = zyfwDict['AddDate'].strftime('%Y-%m-%d %H:%M:%S')
        self.inTime = time.strftime('%Y-%m-%d %H:%M:%S')
        self.sourceType = self.sysconfig.sourceDict.get(unicode(constConfig.zyfwName, 'utf-8'))
        attrList = []
        for i, attr in enumerate(zyfwConfigDict['attr'].split(',')):
            attrDict = {}
            k = self.sysconfig.hsZyfwDict.get(attr.encode('utf-8'))
            v = zyfwDict.get(attr)
            if v != None:
                attrDict[k] = v
                attrDict['i'] = i
                attrList.append(attrDict)

        self.attributeJson = json.dumps(attrList, cls=CJsonEncoder, encoding='utf-8', ensure_ascii=False)
        imgPath = zyfwDict.get(imgField)
        if imgPath != None and imgPath != '':
            imgList.append(config.zyfwFileBasePath + imgPath)
        for fileField in fileFields.split(','):
            filePath = zyfwDict.get(fileField)
            if filePath != None and filePath != '':
                fileList.append(config.zyfwFileBasePath + filePath)

        if len(imgList) != 0:
            try:
                self.savePicPath = self.savePicOrFile(imgList, config.localBasePath, constConfig.libPicPath['1'])
            except Exception as e:
                self.logger.exception(e)

        if len(fileList) != 0:
            try:
                self.saveFilePath = self.savePicOrFile(fileList, config.localBasePath, constConfig.libFilePath['1'])
            except Exception as e:
                self.logger.exception(e)

        return

    def savePicOrFile(self, webPathList, basePath, sTypePath):
        u"""
                从服务器获取文件并保存到本地
                待优化：webSaveFilePath路径更通用一些，本方法优化
        :return:
        """
        str_time = time.strftime('%Y%m%d')
        year_path = os.path.join(basePath, str_time[:4]).replace('\\', '/')
        time_path = os.path.join(year_path, str_time).replace('\\', '/')
        lastPath = os.path.join(time_path, sTypePath).replace('\\', '/')
        FileUtil.mkdir(year_path)
        FileUtil.mkdir(time_path)
        FileUtil.mkdir(lastPath)
        if len(webPathList) == 1:
            fileName = str(uuid.uuid1()).replace('-', '') + '.' + webPathList[0].split('.')[(-1)]
            absolutePath = os.path.join(lastPath, fileName).replace('\\', '/')
            saveFilePath = os.path.join('/temp', str_time[:4], str_time, sTypePath, fileName).replace('\\', '/')
            res = FileUtil.getResponse_requests(webPathList[0])
            if res != None:
                with open(absolutePath, 'wb') as (db_f):
                    for chunk in res.iter_content(chunk_size=512):
                        if chunk:
                            db_f.write(chunk)

        if len(webPathList) != 1:
            fileName = str(uuid.uuid1()).replace('-', '') + '.zip'
            absolutePath = os.path.join(lastPath, fileName).replace('\\', '/')
            saveFilePath = os.path.join('/temp', str_time[:4], str_time, sTypePath, fileName).replace('\\', '/')
            zipUtil = ZipUtil(absolutePath, 'w')
            for webPath in webPathList:
                savePath = os.path.join(lastPath, webPath.split('/')[(-1)]).replace('\\', '/')
                res = FileUtil.getResponse_requests(webPath)
                if res != None:
                    with open(savePath, 'wb') as (db_f):
                        for chunk in res.iter_content(chunk_size=512):
                            if chunk:
                                db_f.write(chunk)

                    arcname = webPath.split('/')[(-1)]
                    zipUtil.addfile(savePath, arcname)

            zipUtil.close()
        return saveFilePath

    def getHsLibraryValueTuple(self):
        u"""
                图书详情表hs_library_
                注意：AddDate格式每个数据表是否都统一
        """
        valueTuple = (
         self.libraryId, constConfig.const_one, self.title, self.savePicPath,
         None, self.author, self.summary, self.attributeJson,
         self.saveFilePath, self.oriTime, self.inTime)
        return valueTuple

    def getHsNewsJorValueTuple(self, *kw):
        u"""
                新闻简表：hs_news_jor
        """
        if self.region != None:
            countryNum = self.sysconfig.countryNumByCountryDict.get(self.region.split(',')[0].encode('utf-8'))
        else:
            countryNum = None
        hsNewsJorValueTuple = (
         self.libraryId, constConfig.const_two, self.title, None,
         None, None, countryNum, None,
         self.sourceType, self.savePicPath, constConfig.const_one, self.oriTime,
         self.inTime, self.inTime)
        return hsNewsJorValueTuple

    def getSolrValueTuple(self, valueTuple):
        u"""
                索引值
        """
        if self.summary != None:
            contentTuple = (
             self.summary, None)
        else:
            contentTuple = (None, None)
        return contentTuple + valueTuple


if __name__ == '__main__':
    pass