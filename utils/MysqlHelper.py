# uncompyle6 version 3.5.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.3 (default, Mar 27 2019, 17:13:21) [MSC v.1915 64 bit (AMD64)]
# Embedded file name: ../src\utils\MysqlHelper.py
# Compiled at: 2019-01-22 20:48:12
u"""
使用方法：1.在主程序中先实例化DB Mysql数据库操作类。
      2.使用方法:db=database()  db.fetch_all("sql")
"""
import pymysql, traceback, utils.Mod_logger as log, config.Config

class MysqlDataBase(object):

    def __init__(self, dbname=None, dbhost=None):
        if dbname is None:
            self._dbname = config.db
        else:
            self._dbname = dbname
        if dbhost is None:
            self._dbhost = config.host
        else:
            self._dbhost = dbhost
        self._dbuser = config.user
        self._dbpassword = config.passwd
        self._dbcharset = config.dbcharset
        self._dbport = int(config.dbport)
        self._conn = self.connectMySQL()
        self._cursor = self._conn.cursor()
        return

    def connectMySQL(self):
        conn = False
        try:
            conn = pymysql.connect(host=self._dbhost, user=self._dbuser, password=self._dbpassword, database=self._dbname, port=self._dbport, charset=self._dbcharset)
            return conn
        except Exception as e:
            raise e

    def executeSql(self, sql, value=None):
        flag = False
        if self._conn:
            try:
                if value == None:
                    self._cursor.execute(sql)
                else:
                    self._cursor.execute(sql, value)
                self._conn.commit()
                flag = True
            except Exception as data:
                flag = False

        return flag

    def executemanySql(self, sql):
        flag = False
        if self._conn:
            try:
                self._cursor.executemany(sql)
                self._conn.commit()
                flag = True
            except Exception as data:
                flag = False

        return flag

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
    db = MysqlDataBase()