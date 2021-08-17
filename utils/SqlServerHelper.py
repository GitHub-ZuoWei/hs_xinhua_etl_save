# uncompyle6 version 3.5.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.3 (default, Mar 27 2019, 17:13:21) [MSC v.1915 64 bit (AMD64)]
# Embedded file name: ../src\utils\SqlServerHelper.py
# Compiled at: 2018-08-27 14:12:09
u"""
使用方法：1.在主程序中先实例化DB Mysql数据库操作类。
      2.使用方法:db=SqlServerDataBase()  db.fetch_all("sql")
"""
import os, sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import pymssql, traceback, config.Config, utils.Mod_logger as log

class SqlServerDataBase(object):

    def __init__(self, dbname=None, dbhost=None):
        if dbname is None:
            self._dbname = config.zyfw_db
        else:
            self._dbname = dbname
        if dbhost is None:
            self._dbhost = config.zyfw_host
        else:
            self._dbhost = dbhost
        self._dbuser = config.zyfw_user
        self._dbpassword = config.zyfw_passwd
        self._dbcharset = config.zyfw_dbcharset
        self._conn = self.connectMySQL()
        self._cursor = self._conn.cursor()
        return

    def connectMySQL(self):
        conn = False
        try:
            conn = pymssql.connect(host=self._dbhost, user=self._dbuser, password=self._dbpassword, database=self._dbname, as_dict=True, charset=self._dbcharset)
            return conn
        except Exception as e:
            print e
            return conn

    def close(self):
        if self._conn:
            try:
                if type(self._cursor) == 'object':
                    self._cursor.close()
                if type(self._conn) == 'object':
                    self._conn.close()
            except Exception as data:
                print data


if __name__ == '__main__':
    try:
        sqlServerDB = SqlServerDataBase()
        dbId = 'dbo.jcms_module_version'
        lastCrawTime = '1900-01-01 00:00:00'
        ZyfwLibSql = "select * from %s where ('%s' <= CONVERT(varchar, AddDate,20)) " % (dbId, lastCrawTime)
        sqlServerDB._cursor.execute(ZyfwLibSql)
        zyfwLists = sqlServerDB._cursor.fetchall()
        print len(zyfwLists)
    except Exception as e:
        traceback.print_exc()
        print e