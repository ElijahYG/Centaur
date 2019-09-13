# -*-conding:utf-8-*-
import datetime
import decimal
import json


class CustomizedEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        elif isinstance(o, datetime.datetime):
            o = o.strftime('%Y-%m-%d %H:%M:%S')
            return o
        elif isinstance(o, datetime.date):
            o = list(o.timetuple())[0:6]
            return o
        else:
            pass
        super(CustomizedEncoder, self).default(o)
