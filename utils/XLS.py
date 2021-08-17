# uncompyle6 version 3.5.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.3 (default, Mar 27 2019, 17:13:21) [MSC v.1915 64 bit (AMD64)]
# Embedded file name: ../src\utils\XLS.py
# Compiled at: 2018-07-13 09:21:42
u"""
Created on 2018年4月22日

@author: 薛清晨
"""
import xlrd

class XLS:

    def __init__(self):
        pass

    def get_tables(self, path):
        u"""
                获取xls表格
        """
        workbook = xlrd.open_workbook(path)
        tables = workbook.sheets()
        return tables

    def get_rows(self, table):
        u"""
                获取表格行数
        """
        nrows = table.nrows
        return nrows

    def get_cols(self, table):
        u"""
                获取表格列数
        """
        ncols = table.ncols
        return ncols