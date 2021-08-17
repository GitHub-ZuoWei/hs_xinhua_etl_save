# uncompyle6 version 3.5.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.5 (default, Apr 19 2019, 17:01:24) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: ../src\sysConfig\SysConfig.py
# Compiled at: 2019-03-18 17:36:55
u"""
Created on 2018年4月15日

@author: mes
"""
import uuid, time
from utils.MysqlHelper import MysqlDataBase
from config import constantConfig as constConfig
import config.Config

class SysConfig(MysqlDataBase):
    u"""
        从后台获取字典（来源、类型、国别等）
       待优化：涉及到的fetchone和fetchall统一一下
    """

    def __init__(self):
        super(SysConfig, self).__init__()
        self.init_sysconfig()

    def init_sysconfig(self):
        self.mediaByMediaSectionDict = {}
        self.languageNumByMediaSectionDict = {}
        self.tagsByMediaSectionDict = {}
        self.countryNumByMediaSectionDict = {}
        self.regionNumByMediaSectionDict = {}
        self.mediaSectionDict = {}
        self.mediaSectionNameDict = {}
        self.mediaSectionIdByNameDict = {}
        self.mediaSectionNameBySectionId = {}
        self.ruleItemDict = {}
        self.fieldDict = {}
        self.sourceDict = {}
        self.regionDict = {}
        self.webFieldDict = {}
        self.countryNumByCountryEnDict = {}
        self.regionByCountryEnDict = {}
        self.countryNumByCountryDict = {}
        self.regionByCountryDict = {}
        self.numByLanguageCodeDict = {}
        self.numByLanguageDict = {}
        self.mediaDict = {}
        self.mediaNameDict = {}
        self.mediaIdByNameDict = {}
        self.mediaNameById = {}
        self.hsZyfwDict = {}
        self.videoTypeDict = {}
        self.fieldRuleLists = []
        self.placeNameList = []
        self.getRegionDict()
        self.getWebFieldDict()
        self.getSourceTypeDict()
        self.getCountryNumByCountryEnDict()
        self.getNumByLanguageCodeDict()
        self.getMediaDict()
        self.getHsZyfwDict()
        self.getVideoType()
        self.getRuleItemDict()
        self.getFieldRule()
        self.getDictOfMediaSection()
        self.getFieldDict()
        self.solrIp = self.getSolrIp()

    def getXhsWebConfig(self):
        u"""
                获取新华社专供配置信息
        """
        xhsWebConfigSql = "select name,url                             from hs_xhs_oem_type                             where                             isDelete = '0' and url is not null"
        self._cursor.execute(xhsWebConfigSql)
        self._conn.commit()
        xhsWebConfigDict = {}
        results = self._cursor.fetchall()
        for row in results:
            xhsWebConfigDict[row[0]] = row[1]

        return xhsWebConfigDict

    def getDictOfMediaSection(self):
        u"""
                根据媒体板块ID获取相关信息
        """
        mediaSectionSql = "select mediaSectionId,    mediaId,    languageNum,    tags,                                   countryNum,    regionNum,    mediaSectionName                                     from hs_media_section                                     where isDelete = '0'"
        self.executeSql(mediaSectionSql)
        results = self._cursor.fetchall()
        for row in results:
            self.mediaByMediaSectionDict[row[0]] = row[1]
            self.languageNumByMediaSectionDict[row[0]] = row[2]
            self.tagsByMediaSectionDict[row[0]] = row[3]
            self.countryNumByMediaSectionDict[row[0]] = row[4]
            self.regionNumByMediaSectionDict[row[0]] = row[5]
            self.mediaSectionDict[row[0]] = '1'
            self.mediaSectionNameDict[row[6]] = '1'
            self.mediaSectionIdByNameDict[row[6]] = row[0]
            self.mediaSectionNameBySectionId[row[0]] = row[6]

    def getFieldRule(self):
        u"""
                获取领域规则
                返回：列表
        """
        fieldRuleSql = "SELECT a.fieldId,GROUP_CONCAT(a.itemId,':',a.contentRelation,':',a.content separator '&')             from hs_field_rule a             LEFT JOIN hs_field b             on a.fieldId = b.fieldId             where a.isDelete = '0' and b.isDelete = '0'             group by a.fieldRelId             ORDER BY b.bk1"
        self.executeSql(fieldRuleSql)
        results = self._cursor.fetchall()
        if len(results) != 0:
            for fieldRule in list(results):
                fieldRuleDict = {}
                fieldRuleItemLists = []
                fieldRuleDict['fieldId'] = fieldRule[0]
                ruleItemLists = fieldRule[1].split('&')
                for ruleItemList in ruleItemLists:
                    fieldRuleItemDict = {}
                    itemId = ruleItemList.split(':')[0]
                    contentRelation = ruleItemList.split(':')[1]
                    content = ruleItemList.split(':')[2]
                    fieldRuleItemDict['contentRelation'] = contentRelation
                    fieldRuleItemDict['itemId'] = self.ruleItemDict[itemId]
                    fieldRuleItemDict[self.ruleItemDict[itemId]] = content
                    fieldRuleItemLists.append(fieldRuleItemDict)

                fieldRuleDict['fieldRuleItem'] = fieldRuleItemLists
                self.fieldRuleLists.append(fieldRuleDict)

    def getVideoType(self):
        u"""
                获取视频分类
        """
        videoTypeSql = "select code,name                         from sys_dictinfo                         where dictkindId =                         ( SELECT dictkindId                             from sys_dictkind                             where code = 'videoType'                         )                         and billStatus = '1'"
        self.executeSql(videoTypeSql)
        results = self._cursor.fetchall()
        for row in results:
            self.videoTypeDict[row[1].encode('utf-8')] = row[0]

    def getSolrIp(self):
        u"""
                获取solr所在的IP地址
        """
        SolrIpSql = "select coValue from sys_config where code = 'SOLRIP'"
        self.executeSql(SolrIpSql)
        results = self._cursor.fetchone()
        return results[0]

    def getHsZyfwDict(self):
        u"""
                获取知远防务字段字典
        """
        hsZyfwDictSql = "select * from hs_zyfw_dict where isDelete = '0'"
        self.executeSql(hsZyfwDictSql)
        results = self._cursor.fetchall()
        for result in results:
            self.hsZyfwDict[result[0]] = result[1]

    def getMediaDict(self):
        u"""
                获取mediaId字典和media媒体名称字典
        """
        mediaDictSql = "select mediaId,mediaName from hs_media where isDelete = '0'"
        self.executeSql(mediaDictSql)
        results = self._cursor.fetchall()
        for row in results:
            self.mediaDict[row[0]] = '1'
            self.mediaNameDict[row[1]] = '1'
            self.mediaIdByNameDict[row[1]] = row[0]
            self.mediaNameById[row[0]] = row[1]

    def getRegionDict(self):
        u"""
                获取地域编号字典
        """
        RegionDictSql = "select code,name                          from sys_dictinfo                          where dictkindId =                          (                              SELECT dictkindId                              from sys_dictkind                              where code = 'webCountryType'                         )"
        self.executeSql(RegionDictSql)
        results = self._cursor.fetchall()
        for row in results:
            self.regionDict[row[0].encode('utf-8')] = row[1].encode('utf-8')

    def getWebFieldDict(self):
        u"""
                获取领域类型字典
        """
        webFieldDictSql = "select code,name                            from sys_dictinfo                            where dictkindId =                            (                                SELECT dictkindId                                from sys_dictkind                                where code = 'webFieldType'                            )"
        self.executeSql(webFieldDictSql)
        results = self._cursor.fetchall()
        for row in results:
            self.webFieldDict[row[1].encode('utf-8')] = row[0].encode('utf-8')

    def getCountryNumByCountryEnDict(self):
        u"""
                根据国家英文获取国家编号字典
        """
        CountryDictSql = 'select number,countryKeys,region,internetName,                           region                           from hs_country '
        self.executeSql(CountryDictSql)
        results = self._cursor.fetchall()
        for row in results:
            self.countryNumByCountryEnDict[row[1]] = str(row[0])
            self.regionByCountryEnDict[row[1].encode('utf-8')] = row[2]
            for name in row[3].encode('utf-8').split('、'):
                self.countryNumByCountryDict[name] = str(row[0])

            for name in row[3].encode('utf-8').split('、'):
                self.regionByCountryDict[name] = row[4]

    def getNumByLanguageCodeDict(self):
        u"""
                获取语种编号字典code：number
        """
        languageSql = 'select number,code,language                        from hs_languages '
        self.executeSql(languageSql)
        results = self._cursor.fetchall()
        for row in results:
            self.numByLanguageCodeDict[row[1]] = str(row[0])
            for lan in row[2].encode('utf-8').split('、'):
                self.numByLanguageDict[lan] = str(row[0])

    def getSourceTypeDict(self):
        u"""
                获取来源类型字典
        """
        sourceTypeSql = 'select sourceName,sourceCode from hs_source '
        self.executeSql(sourceTypeSql)
        results = self._cursor.fetchall()
        for row in results:
            self.sourceDict[row[0]] = str(row[1])

    def getHsLibraryConfig(self):
        u"""
                获取数字图书馆配置信息
        """
        hsLibraryConfigSql = "SELECT * from hs_library_config where isDelete = '0' and isSpider = '1' and dbCount != 0"
        libConfigLists = []
        self.executeSql(hsLibraryConfigSql)
        results = self._cursor.fetchall()
        for libList in results:
            libraryConfigDict = {}
            libraryConfigDict['dbId'] = libList[0]
            libraryConfigDict['dbName'] = libList[1]
            libraryConfigDict['dbCount'] = libList[2]
            libraryConfigDict['lastSpiderCount'] = libList[3]
            libraryConfigDict['bookNameLine'] = libList[4]
            libraryConfigDict['abstractLine'] = libList[5]
            libraryConfigDict['bookDataTimeLine'] = libList[6]
            libraryConfigDict['authorLine'] = libList[7]
            libraryConfigDict['publisherLine'] = libList[8]
            libraryConfigDict['languageLine'] = libList[9]
            libraryConfigDict['withoutLine'] = libList[10]
            libraryConfigDict['classLine'] = libList[11]
            libraryConfigDict['isSpider'] = libList[12]
            libraryConfigDict['isDelete'] = libList[13]
            libConfigLists.append(libraryConfigDict)

        return libConfigLists

    def getHsZyfwConfig(self):
        u"""
                获取知远防务配置信息
        """
        hsZyfwConfigSql = "SELECT * from hs_zyfw_config where isDelete = '0' and isSpider = '1'"
        zyfwConfigLists = []
        self.executeSql(hsZyfwConfigSql)
        results = self._cursor.fetchall()
        for libList in results:
            zyfwConfigDict = {}
            zyfwConfigDict['dbId'] = libList[0]
            zyfwConfigDict['dbName'] = libList[1]
            zyfwConfigDict['imgField'] = libList[2]
            zyfwConfigDict['fileField'] = libList[3]
            zyfwConfigDict['isSpider'] = libList[4]
            zyfwConfigDict['isDelete'] = libList[5]
            zyfwConfigDict['sType'] = libList[6]
            zyfwConfigDict['attr'] = libList[7]
            zyfwConfigDict['lastCrawTime'] = libList[8]
            zyfwConfigLists.append(zyfwConfigDict)

        return zyfwConfigLists

    def getFieldDict(self):
        u"""
                获取领域字典
        key:为hs_field的fieldName
        value:为hs_field的fieldId
        """
        fieldSql = 'SELECT fieldName,fieldId from hs_field '
        self.executeSql(fieldSql)
        results = self._cursor.fetchall()
        for row in results:
            self.fieldDict[row[0]] = str(row[1])

    def getRuleItemDict(self):
        u"""
                获取领域规则枚举字典
        key:为hs_field_rule_item的主键
        value:为spiderName 抽取的字段名字
        """
        ruleItemSql = 'SELECT id,spiderName from hs_field_rule_item '
        self.executeSql(ruleItemSql)
        results = self._cursor.fetchall()
        for row in results:
            self.ruleItemDict[row[0]] = str(row[1])

    def getCountOfTable(self, tableName):
        u"""
                获取表数据总数
        """
        CountOfTable = 'SELECT count(*) from %s' % tableName
        self.executeSql(CountOfTable)
        result = self._cursor.fetchone()
        return result[0]

    def getMaxValueOfDynamicTable(self, Fixed_name):
        u"""
                获取动态表数据最大的动态值
        """
        MaxValueOfDynamicTableSql = "SELECT MAX(dynamic_name + 0) from hs_dynamic_table_name WHERE Fixed_name = '%s'" % Fixed_name
        self.executeSql(MaxValueOfDynamicTableSql)
        result = self._cursor.fetchone()
        return result[0]

    def fieldTypeByRule(self, *kw):
        u"""
                根据领域规则清洗得到所属领域
        kw:参数先后顺序为：国家，来源，媒体板块、媒体板块标签、媒体、语种、中图分类号、新华网专供子栏目、知远防务子栏目,标题加内容
        return:领域编号
        """
        countryNum = kw[0] if kw[0] != None else ''
        sourceType = kw[1] if kw[1] != None else ''
        mediaSectionId = kw[2] if kw[2] != None else ''
        tags = kw[3] if kw[3] != None else ''
        mediaId = kw[4] if kw[4] != None else ''
        languageType = kw[5] if kw[5] != None else ''
        libraryClass = kw[6] if kw[6] != None else ''
        xhsClass = kw[7] if kw[7] != None else ''
        zyfwClass = kw[8] if kw[8] != None else ''
        keywords = kw[9] if kw[9] != None else ''
        if self.fieldRuleLists != None:
            for fieldRuleDict in self.fieldRuleLists:
                flag = 0
                fieldId = fieldRuleDict['fieldId']
                fieldRuleItemLists = fieldRuleDict['fieldRuleItem']
                for fieldRuleItemDict in fieldRuleItemLists:
                    contentRelation = fieldRuleItemDict['contentRelation']
                    itemName = fieldRuleItemDict['itemId']
                    contentLists = fieldRuleItemDict[itemName].strip().split(';')
                    if isinstance(locals()[itemName], str) is False:
                        itemContent = locals()[itemName].encode('utf-8', 'ignore')
                    else:
                        itemContent = locals()[itemName]
                    notEqflag = 1
                    for contentOftable in contentLists:
                        flag = 0
                        contentOftable = contentOftable.encode('utf-8', 'ignore')
                        if contentRelation == '1' and contentOftable == itemContent:
                            flag = 1
                        elif contentRelation == '0' and contentOftable in itemContent:
                            notEqflag = 0
                            break
                        elif contentRelation == '2':
                            if contentOftable in itemContent:
                                flag = 1
                        if flag == 1:
                            break

                    if contentRelation == '0' and notEqflag == 1:
                        flag = 1
                    if flag == 0:
                        break

                if flag == 1:
                    return fieldId

        return

    def getDynamicTable(self, *kw):
        u"""
                获取动态表的最大的一张表值
        """
        prefixTableName = kw[0]
        maxValue = self.getMaxValueOfDynamicTable(prefixTableName)
        maxValue = int(maxValue)
        if self.getCountOfTable(prefixTableName + str(maxValue)) >= int(config.divisionNum):
            if prefixTableName == constConfig.prefixNameOfNewsTable:
                self.executeSql(constConfig.createHsNewsTableSql, maxValue + 1)
            else:
                self.executeSql(constConfig.createHsLibraryTable, maxValue + 1)
            self.executeSql(constConfig.insertHsDynamicTableNameSql, (str(uuid.uuid1()).replace('-', ''), prefixTableName, maxValue + 1, time.strftime('%Y-%m-%d %H:%M:%S')))
        return str(maxValue)

    def getPlaceName(self):
        u"""
                获取地名
        """
        placeNameSql = 'SELECT district_name from hs_place_name'
        self.executeSql(placeNameSql)
        results = self._cursor.fetchall()
        for result in results:
            self.placeNameList.append(result[0].encode('utf8'))

    def solrInfoDict(self, sorlTuple):
        u"""
        solr信息字典化
        """
        solrDict = {}
        solrDict['newsContent'] = sorlTuple[0]
        solrDict['downloadLinks'] = sorlTuple[1]
        solrDict['id'] = sorlTuple[2]
        solrDict['type'] = sorlTuple[3]
        solrDict['title'] = sorlTuple[4]
        solrDict['mediaSectionId'] = sorlTuple[5]
        solrDict['fieldType'] = sorlTuple[6]
        solrDict['libaryFieldType'] = sorlTuple[7]
        solrDict['countryType'] = sorlTuple[8]
        solrDict['languageType'] = sorlTuple[9]
        solrDict['sourceType'] = int(sorlTuple[10])
        solrDict['coverPhoto'] = sorlTuple[11]
        solrDict['oriTime'] = sorlTuple[13]
        solrDict['sortTime'] = sorlTuple[14]
        solrDict['inTime'] = sorlTuple[14]
        return solrDict


if __name__ == '__main__':
    try:
        sysconfig = SysConfig()
        content = '中国的二手车市场正在迅速扩大。2018年的二手车销量预计同比增长约13％，达到1400万辆，较5年前增长约3倍。相比之下，新车市场的销售业绩则时隔28年再次出现同比下降。专用二手车交易APP不断上线，推动了中国二手车的销量，运营这类软件的新创企业也在不断增加。预计还将影响到全球最大的新车市场。'
        print sysconfig.fieldTypeByRule(None, None, None, None, None, None, None, None, None, content)
        print sysconfig.fieldRuleLists
    except (Exception,) as e:
        print e