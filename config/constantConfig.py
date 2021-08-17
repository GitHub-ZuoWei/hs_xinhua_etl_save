# uncompyle6 version 3.5.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.5 (default, Apr 19 2019, 17:01:24) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: ../src\config\constantConfig.py
# Compiled at: 2019-03-18 16:58:57
import config.Config as config

libPicPath = {}
libFilePath = {}
videoPicPath = 'video/pic'
videoFilePath = 'video/file'
Korea_sourceDict = {}
hsNewsJorSql = 'INSERT INTO hs_data_jor             (id,            type,             title,        mediaSectionId,              fieldType,     libaryFieldType,  countryType,  languageType,              sourceType,    coverPhoto,       isToJor,    oriTime,             inTime,        realInTime,    tableCode)              VALUES (%s,%s,%s,%s,                      %s,%s,%s,%s,                      %s,%s,%s,%s,                      %s,%s,%s)'
hsNewsSql = '(id,        isToJor,    chineseTitle,    newsTime,            content,    img,        downloadLinks,   url,             isDelete,   dataTime,   transTitle,      transContent,             operateTime,bk2,bk1)              VALUES (%s,%s,%s,%s,                      %s,%s,%s,%s,                      %s,%s,%s,%s,                      %s,%s,%s)'
hsLibrarySql = '(libraryId,        isToJor,    title,        coverPhoto,                  fieldType,        author,     introduction, attributes,                  downloadLinks,    oriTime,    inTime)                  VALUES (%s,%s,%s,%s,                          %s,%s,%s,%s,                          %s,%s,%s)'
spiderTxsTagsSql = 'INSERT INTO spider_txs_tags                     (id,    tag,    operateTime)                     VALUES                     (%s,    %s,    %s)'
hsJoseonSql = 'INSERT INTO hs_joseon                 (joseonId,    newsTitle,    newsTime,    content,                  sourceType,  isDelete,    operateTime)                  VALUES (%s,%s,%s,%s,                          %s,%s,%s)'
hsCountrySql = 'INSERT INTO hs_country                 (countryId,        number,        countryName,    internetName,                  countryFullName,  countryKeys,   region,         initials,                  spellFull,        spellFirst,    isDelete)                  VALUES (%s,%s,%s,%s,                          %s,%s,%s,%s,                          %s,%s,%s)'
hsMediaSql = 'INSERT INTO hs_media              (mediaId,    mediaName,    countryNum,    isDelete,               operateTime)               VALUES (%s,%s,%s,%s,                       %s)'
dataStatisticSql = 'replace INTO hs_internet_data_statistics             (id,        fileName,        counts,        oriTime,              inTime)              VALUES (%s,%s,%s,%s,                      %s)'
hsToolsSql = 'replace INTO hs_tools                     (id,contentForExport,encoding,siteCofName,                      title,url,isDelete,operateTime)                      VALUES (%s,%s,%s,%s,                              %s,%s,%s,%s)'
updateMediaSql = "update hs_media                     set mediaName = %s , countryNum = %s, operateTime = %s, isDelete = '0'                     where mediaId = %s"
hsMediaSectionInsertSql = 'INSERT INTO hs_media_section                             (mediaSectionId,    mediaId,     mediaSectionName,    tags,                             language,           languageNum, countryName,         countryEng,                             countryNum,         region,      regionNum,           isHot,                             isDelete,           operateTime, siteDataTime)                             VALUES (%s,%s,%s,%s,                                     %s,%s,%s,%s,                                     %s,%s,%s,%s,                                     %s,%s,%s)'
hsMediaSectionUpdateSql = 'update hs_media_section                             set tags = %s,        language = %s,    languageNum = %s,    countryName = %s,                                 countryEng = %s,  countryNum = %s,  region = %s,         regionNum = %s,                                 isHot = %s,       isDelete = %s,    operateTime = %s,  siteDataTime = %s,                                 mediaSectionName = %s where mediaSectionId = %s'
deleteMediaIdSql = 'delete from hs_media where mediaId = %s'
deleteMediaNameSql = 'delete from hs_media where mediaName = %s'
deleteMediaSectionSql = 'delete from hs_media_section where mediaSectionId = %s'
deleteMediaSectionNameSql = 'delete from hs_media_section where mediaSectionName = %s'
insertHsVideoSql = 'INSERT INTO hs_video                     (videoId,    title,      videoType,    tag,                      content,    img_url,    temp_url,    orgin_url,                      oriTime,    inTime,     isDelete)                     VALUES (%s,%s,%s,%s,                              %s,%s,%s,%s,                              %s,%s,%s)'
hsLibraryConfigSql = 'INSERT INTO hs_library_config                         (dbId,            dbName,    dbCount,    lastSpiderCount,                          bookNameLine,    isSpider,  isDelete,   dataTime)                          VALUES (%s,%s,%s,%s,                                  %s,%s,%s,%s)'
hsLibrarySql = '(libraryId,     isToJor,    title,        coverPhoto,                  fieldType,     author,     introduction, attributes,                  downloadLinks, oriTime,    inTime)                  VALUES (%s,%s,%s,%s,                          %s,%s,%s,%s,                          %s,%s,%s)'
insertHsDynamicTableNameSql = 'INSERT INTO hs_dynamic_table_name                          (Data_Table_Collection_id,    Fixed_name,    dynamic_name,    Creation_time)                           VALUES (%s,%s,%s,%s)'
createHsNewsTableSql = " CREATE TABLE `hs_news_%s` (  `id` varchar(32) CHARACTER SET utf8 NOT NULL DEFAULT '',  `isToJor` char(1) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT '是否在简版中显示',  `chineseTitle` text CHARACTER SET utf8mb4 COMMENT '中文标题',  `englishTitle` text CHARACTER SET utf8mb4 COMMENT '英文标题',  `transTitle` text CHARACTER SET utf8mb4 COMMENT '翻译后的标题',  `newsTime` varchar(19) CHARACTER SET utf8 DEFAULT NULL COMMENT '新闻时间',  `content` longtext COLLATE utf8mb4_unicode_ci COMMENT '新闻内容',  `author` varchar(1024) CHARACTER SET utf8 DEFAULT NULL COMMENT '作者（中文）',  `authorUnit` varchar(64) CHARACTER SET utf8 DEFAULT NULL COMMENT '作者单位',  `translator` varchar(64) CHARACTER SET utf8 DEFAULT NULL COMMENT '翻译者',  `tags` varchar(512) CHARACTER SET utf8 DEFAULT NULL COMMENT '新闻标签',  `img` text CHARACTER SET utf8 COMMENT '图片地址',  `dataTime` varchar(19) CHARACTER SET utf8 DEFAULT NULL COMMENT '入库时间',  `url` text CHARACTER SET utf8 COMMENT '新闻网址',  `bk1` varchar(512) CHARACTER SET utf8 DEFAULT NULL,  `bk2` varchar(512) CHARACTER SET utf8 DEFAULT NULL,  `bk3` varchar(512) CHARACTER SET utf8 DEFAULT NULL,  `isDelete` char(1) CHARACTER SET utf8 DEFAULT NULL,  `operatorId` varchar(32) CHARACTER SET utf8 DEFAULT NULL,  `operateTime` varchar(19) CHARACTER SET utf8 DEFAULT NULL,  `downloadLinks` text CHARACTER SET utf8 COMMENT '下载链接',  `transContent` longtext CHARACTER SET utf8mb4 COMMENT '翻译后的内容',  `author2` varchar(64) CHARACTER SET utf8 DEFAULT NULL COMMENT '作者（英文）',  PRIMARY KEY (`id`),  KEY `1` (`isToJor`,`dataTime`) USING BTREE) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;"
createHsLibraryTable = " CREATE TABLE `hs_library_%s` (  `libraryId` varchar(32) NOT NULL,  `isToJor` char(1) DEFAULT NULL COMMENT '是否在简版中显示',  `title` varchar(256) DEFAULT NULL COMMENT '书名',  `coverPhoto` varchar(256) DEFAULT NULL COMMENT '封面图片',  `fieldType` varchar(32) DEFAULT NULL COMMENT '中图分类号',  `author` varchar(256) DEFAULT NULL COMMENT '作者',  `introduction` longtext COMMENT '简介或摘要 --solr搜索时用的',  `attributes` longtext COMMENT '所有的属性',  `downloadLinks` varchar(256) DEFAULT NULL COMMENT '下载链接',  `oriTime` varchar(19) DEFAULT NULL COMMENT '原始时间',  `inTime` varchar(19) DEFAULT NULL COMMENT '入库时间',  PRIMARY KEY (`libraryId`)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='图书';"
redis_txs = 'queue:txshe'
redis_txs_titles = 'txs_titles'
redis_txs_titleField = 'txs_titleField'
redis_library_dbRid = 'queue:library_dbRid_q'
redis_library_config = 'queue:library_config_q'
redis_library_files = 'queue:library_files'
redis_internet_zip = 'queue:internet_zip'
redis_internet_titles = 'queue:internet_titles'
redis_internet_files = 'queue:internet_files'
redis_internet_siteDateTime = 'string:internet_siteDateTime'
redis_jsfw_zip = 'queue:jsfw_zip'
redis_jsfw_titles = 'queue:jsfw_titles'
redis_video_list_set = 'queue:video_list_set'
redis_video_list = 'queue:video_list_q'
redis_zyfw_dbId = 'queue:zyfw_dbId'
redis_anTianSecurity_zip = 'anTianSecurity_zip'
redis_anTianSecurity_files = 'anTianSecurity_files'
redis_anTianSecurity_titles = 'anTianSecurity_titles'
redis_xhs_dict = {}
internetName = '互联网'
digitLibName = '数字图书馆'
jsfwName = '简氏防务'
zyfwName = '知远防务'
xhsName = '新华网专供'
weiXinName = '微信公众号'
internetFile = 'articleData.txt'
toolDataId = '9b57c45037134425921a1a7f16a3741b'
toolGuid = '757a04adeb3648588d286a6605d2d608'
internetReg = 'dataInfo.zip'
internetRelationFile = 'siteCofData.txt'
AnTianSecurityReges = '.zip'
jsfw_reges = '.zip'
weiXinMediaId = 'c539e686edf25845b893f83af27eebc5'
const_zero = '0'
const_one = '1'
const_two = '2'
prefixNameOfLibraryTable = 'hs_library_'
prefixNameOfNewsTable = 'hs_news_'
flushCountry = 'http://' + config.webIP + ':' + config.webPORT + '/flushStaticData?keys=countrys'
flushMedia = 'http://' + config.webIP + ':' + config.webPORT + '/flushStaticData?keys=medias'
flushWeather = 'http://' + config.webIP + ':' + config.webPORT + '/flushStaticData?keys=homeWeather'
nlpUrl = 'http://' + config.webIP + ':8082'
chineseNewsClassifyUrl = nlpUrl + '/chineseNewsClassify'
chineseSentimentAnalysisUrl = nlpUrl + '/chineseSentimentAnalysis'
classifyLabels = ['__label__affairs', '__label__economic', '__label__edu', '__label__science']
if __name__ == '__main__':
    pass
