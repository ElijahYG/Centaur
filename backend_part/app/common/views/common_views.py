#!usr/bin/env python
# -*- coding: utf-8 -*-
"""
@version:
author:yanggang
@time: 2019/01/22
@file: auth.py
@function:
@modify:
"""
import json
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from backend_part.lib.CustomizedEncoder import CustomizedEncoder


def _response_json(json_data):
    return HttpResponse(json.dumps(json_data, cls=CustomizedEncoder), 'text/plain')

