#!usr/bin/env python
# -*- coding: utf-8 -*-
"""
@version:
author:yanggang
@time: 2019/01/31
@file: decorate.py
@function:
@modify:
"""
from django.http import JsonResponse


def permission_control(model="app"):
    """
    权限检查
    :param model:
    :return:
    """

    def check_group(input_function):
        def check_function(*args, **kwargs):
            request = args[0]
            path = request.path
            permission = model + "." + path.strip("/")
            print('current permission: ', permission)
            print('is current user has ')
            if request.user.has_perm(permission):
                return input_function(*args, **kwargs)

            return JsonResponse({"status": "403", "msg": "Sorry, Current User has no permission!"})

        return check_function

    return check_group
