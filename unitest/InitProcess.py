# uncompyle6 version 3.5.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.5 (default, Apr 19 2019, 17:01:24) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: ../src\unitest\InitProcess.py
# Compiled at: 2019-01-19 15:01:48
u"""
Created on 2018年6月6日

@author: mes
"""
import config.Config
from utils.MysqlHelper import MysqlDataBase
from utils.RedisQueue import RedisQueue
try:
    mysqldb = MysqlDataBase()
    delete_hs_data_jor = 'DELETE from hs_data_jor'
    delete_hs_news_1000 = 'DELETE from hs_news_1000'
    delete_hs_library_1000 = 'DELETE from hs_library_1000'
    delete_hs_joseon = 'DELETE from hs_joseon'
    delete_hs_joseon_entourage = 'DELETE from hs_joseon_entourage'
    mysqldb.executeSql(delete_hs_data_jor)
    mysqldb.executeSql(delete_hs_news_1000)
    mysqldb.executeSql(delete_hs_library_1000)
    mysqldb.executeSql(delete_hs_joseon)
    mysqldb.executeSql(delete_hs_joseon_entourage)
    print 'done\n'
except Exception as e:
    print e