# uncompyle6 version 3.5.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.5 (default, Apr 19 2019, 17:01:24) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: ../src\test\FieldClassify.py
# Compiled at: 2019-01-25 16:06:24
u"""
Created on 2019年1月25日

@author: mes
"""
from utils.MysqlHelper import MysqlDataBase

class FieldClassify(MysqlDataBase):
    u"""
        重新按照领域规则进行分类
    """

    def __init__(self, solrIp):
        """
        Constructor
        """
        super(FieldClassify, self).__init__()
        self.solrIp = solrIp
        solr = pysolr.Solr(self.solrIp)
        solrCoreAdmin = pysolr.SolrCoreAdmin(self.solrIp)
        print solrCoreAdmin.status()


if __name__ == '__main__':
    pass