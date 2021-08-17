# uncompyle6 version 3.5.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.3 (default, Mar 27 2019, 17:13:21) [MSC v.1915 64 bit (AMD64)]
# Embedded file name: ../src\utils\CJsonEncoder.py
# Compiled at: 2018-07-13 09:21:42
import json
from datetime import date, datetime

class CJsonEncoder(json.JSONEncoder):
    u"""
        重写构造json类，遇到日期特殊处理，其余的用内置的就行
    """

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            if isinstance(obj, date):
                return obj.strftime('%Y-%m-%d')
            return json.JSONEncoder.default(self, obj)