# uncompyle6 version 3.5.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.5 (default, Apr 19 2019, 17:01:24) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: ../src\digitLib\DigitLibJSON.py
# Compiled at: 2019-04-23 16:55:54
u"""
Created on 2018年4月15日

@author: mes
"""
import uuid, time, re, json, os, sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import config.Config
from utils.CJsonEncoder import CJsonEncoder
from utils.FileUtil import FileUtil
import config.constantConfig as constConfig
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

class DigitLibJSON(object):
    u"""
        数字图书馆JSON数据解析
    """

    def __init__(self):
        self.__item_start_flag = '<REC>'
        self.__p = re.compile('^<(.*)>=(.*)$')
        self.__digitLanguageDict = {}

    def parseAllDBInfo(self, data):
        u"""
                解析trsdb.json文件
        """
        dataList = data.split('\t')
        self.__trsDbId = dataList[0]
        self.__dbName = dataList[1]
        self.__dbCount = dataList[2]

    def parseLibInfo(self, libDict):
        u"""
                解析每个数据库
        """
        libDict = eval(libDict)
        self.__dbId = libDict['dbId']
        self.__rid = libDict['rid']
        self.__inTime = time.strftime('%Y-%m-%d %H:%M:%S')
        self._libraryId = self.__dbId + '_' + self.__rid
        contentPath = config.digitLib_db_info + str(libDict['dbId']) + '&start=' + str(libDict['rid']) + '&count=1'
        res = FileUtil.getResponse_requests(contentPath)
        if res != None:
            res_content = res.content
            res_lists = res_content.split('\n')
            flag = 0
            attributeFlag = 1
            attributeDict = {}
            attrList = []
            attribute = ''
            self.__title = None
            self.__rid = None
            self.__author = None
            self.__publisher = None
            self.__language = ''
            self.__abstract = None
            self.__bookDataTime = ''
            self.__libClass = None
            value = ''
            for i in xrange(1, len(res_lists)):
                data = res_lists[i].strip()
                if data != self.__item_start_flag:
                    m = self.__p.match(data)
                    if m != None:
                        if attributeFlag == 0:
                            if flag == libDict['abstractLine']:
                                self.__abstract = value.replace('\\t', ' ')
                            elif libDict['withoutLine'] != None:
                                if str(flag) not in libDict['withoutLine'].split(','):
                                    attributeDict[attribute] = value
                                    attributeDict['i'] = i
                                    attrList.append(attributeDict)
                                    attributeDict = {}
                            else:
                                attributeDict[attribute] = value
                                attributeDict['i'] = i
                                attrList.append(attributeDict)
                                attributeDict = {}
                            attributeFlag = 1
                        flag += 1
                        attribute = m.group(1).strip()
                        value = m.group(2).strip()
                        if flag == libDict['bookNameLine']:
                            self.__title = value
                        elif flag == libDict['abstractLine']:
                            self.__abstract = value
                        elif len(value) != 0 and libDict['withoutLine'] != None:
                            if str(flag) not in libDict['withoutLine'].split(','):
                                attributeDict[attribute] = value
                                attributeDict['i'] = i
                                attrList.append(attributeDict)
                                attributeDict = {}
                        else:
                            attributeDict[attribute] = value
                            attributeDict['i'] = i
                            attrList.append(attributeDict)
                            attributeDict = {}
                        if attribute == 'RID':
                            self.__rid = value
                        if flag == libDict['authorLine']:
                            self.__author = value
                        if flag == libDict['publisherLine']:
                            self.__publisher = value
                        if flag == libDict['languageLine']:
                            self.__language = value
                        if flag == libDict['abstractLine']:
                            self.__abstract = value
                        if flag == libDict['classLine']:
                            self.__libClass = value
                        if flag == libDict['bookDataTimeLine']:
                            self.__bookDataTime = value[:4]
                    else:
                        attributeFlag = 0
                        value = value + '\n' + data

            self.__attributeJson = json.dumps(attrList, cls=CJsonEncoder, ensure_ascii=False)
        return

    @property
    def getTrsDbId(self):
        return self.__trsDbId

    @property
    def getDbId(self):
        return self.__dbId

    @property
    def getRid(self):
        return self.__rid

    @property
    def getLibraryId(self):
        return self._libraryId

    @property
    def getTitle(self):
        return self.__title

    def savePicOrFile(self, webPath, basePath, sTypePath):
        u"""
                从服务器获取文件并保存到本地
        :return:null
        """
        res = FileUtil.getResponse_requests(webPath)
        if res is None:
            return
        else:
            headersDict = eval(str(res.headers))
            if headersDict.has_key('Content-Disposition'):
                fileType = headersDict['Content-Disposition'].split('filename=')[1].split('.')[1]
                fileName = self._libraryId + '.' + fileType
            elif headersDict.has_key('Content-Type'):
                fileType = headersDict['Content-Type'].split('/')[1].split(';')[0]
                fileName = self._libraryId + '.' + fileType
            else:
                return
            str_time = time.strftime('%Y%m%d')
            year_path = os.path.join(basePath, str_time[:4]).replace('\\', '/')
            time_path = os.path.join(year_path, str_time).replace('\\', '/')
            lastPath = os.path.join(time_path, sTypePath).replace('\\', '/')
            FileUtil.mkdir(year_path)
            FileUtil.mkdir(time_path)
            FileUtil.mkdir(lastPath)
            absolutePath = os.path.join(lastPath, fileName).replace('\\', '/')
            saveFilePath = os.path.join('/temp', str_time[:4], str_time, sTypePath, fileName).replace('\\', '/')
            with open(absolutePath, 'wb') as (db_f):
                for chunk in res.iter_content(chunk_size=512):
                    if chunk:
                        db_f.write(chunk)

            return saveFilePath

    def getHsLibraryConfigValueTuple(self, *kw):
        u"""
        hs_library_config表值
        """
        inTime = time.strftime('%Y-%m-%d %H:%M:%S')
        valueTuple = (self.__trsDbId, self.__dbName, self.__dbCount, 0,
         int(constConfig.const_two), constConfig.const_zero, constConfig.const_zero, inTime)
        return valueTuple

    def getHsLibraryValueTuple(self, *kw):
        u"""
                图书详情表hs_library_1000
        """
        self.__libraryId = str(uuid.uuid1()).replace('-', '')
        self.__oriTime = None
        if self.__bookDataTime.isdigit() and self.__bookDataTime != None and self.__bookDataTime != '':
            self.__oriTime = self.__bookDataTime
        valueTuple = (self.__libraryId, constConfig.const_one, self.__title, self.localPicPath,
         self.__libClass, self.__author, self.__abstract, self.__attributeJson,
         self.localFilePath, self.__oriTime, self.__inTime)
        return valueTuple

    def getHsNewsJorValueTuple(self, *kw):
        u"""
                新闻简表：hs_news_jor
        """
        languageCode = self.__digitLanguageDict.get(self.__language.lower())
        languageNumber = None
        countryType = None
        sourceType = self.sysconfig.sourceDict.get(unicode(constConfig.digitLibName, 'utf-8'))
        if languageCode != None and languageCode != '':
            languageNumber = self.sysconfig.numByLanguageCodeDict.get(languageCode)
        else:
            languageNumber = self.sysconfig.numByLanguageCodeDict.get(self.__language.lower())
        fieldType = self.sysconfig.fieldTypeByRule(None, sourceType, None, None, None, languageNumber, self.__libClass, None, None, None)
        if fieldType != None:
            fieldType = fieldType.encode('utf-8')
        valueTuple = (
         self.__libraryId, constConfig.const_two, self.__title.decode('utf-8', 'ignore'), None,
         fieldType, self.__libClass, countryType, languageNumber,
         sourceType, self.localPicPath, constConfig.const_one, self.__oriTime,
         self.__inTime, self.__inTime)
        return valueTuple

    def getSolrValueTuple(self, valueTuple):
        u"""
                索引值
        """
        if self.__abstract != None:
            contentTuple = (
             self.__abstract.decode('utf-8', 'ignore'), None)
        else:
            contentTuple = (None, None)
        return contentTuple + valueTuple

    def updateHsLibraryConfig(self, *kw):
        u"""
                更新数字图书馆数据解析的位置
        """
        dataTime = time.strftime('%Y-%m-%d %H:%M:%S')
        hsLibraryConfigSql = "update hs_library_config set lastSpiderCount = '%s',dataTime = '%s' where dbId= '%s'" % (kw[0], dataTime, kw[1])
        self.sysconfig._cursor.execute(hsLibraryConfigSql)
        self.sysconfig._conn.commit()


if __name__ == '__main__':
    pass