# /usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = "Elijah"
__date__ = "2019/6/24 14:08"

import json
from django.http import HttpResponse
from email.mime.text import MIMEText
from backend_part.lib.decorate import permission_control
from django.contrib.auth import authenticate, login, logout
from backend_part.lib.CustomizedEncoder import CustomizedEncoder
from django.contrib.auth.models import User, Group, Permission, ContentType


def _response_json(json_data):
    return HttpResponse(json.dumps(json_data, cls=CustomizedEncoder), 'text/plain')


def sample_table(request):
    """
    表格
    :param request:
    :return:
    """
    pass
