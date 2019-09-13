#!usr/bin/env python
# -*- coding: utf-8 -*-
"""
@version:
author:yanggang
@time: 2019/01/30
@file: auth_test_views.py
@function:
@modify:
"""

import json
import smtplib
from django.http import HttpResponse
from email.mime.text import MIMEText
from django.contrib.auth import authenticate, login, logout
from backend_part.lib.CustomizedEncoder import CustomizedEncoder
from django.contrib.auth.models import User, Group, Permission, ContentType
from django.contrib.auth.decorators import permission_required
from backend_part.lib.decorate import permission_control
from django.contrib.auth.decorators import login_required


def _response_json(json_data):
    return HttpResponse(json.dumps(json_data, cls=CustomizedEncoder), 'text/plain')


# @permission_control(model='app')

@login_required
def test_get_users(request):
    """
    测试
    :return:
    """
    try:
        ret = User.objects.all()
        data = [{"id": i.id, "username": i.username, "last_login": i.last_login, "email": i.email,
                 "is_active": str(i.is_active)} for i in ret]
        result = {"status": 200, "data": data, "msg": "Test Success"}
        return _response_json(result)
    except Exception as e:
        print(e)
        result = {"status": 400, "msg": e}
        return _response_json(result)
