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
import smtplib
from django.http import HttpResponse
from email.mime.text import MIMEText
from backend_part.lib.decorate import permission_control
from django.contrib.auth import authenticate, login, logout
from backend_part.lib.CustomizedEncoder import CustomizedEncoder
from django.contrib.auth.models import User, Group, Permission, ContentType

import sys


# reload(sys)
# sys.setdefaultencoding('utf8')


def _response_json(json_data):
    return HttpResponse(json.dumps(json_data, cls=CustomizedEncoder), 'text/plain')


def user_login(request):
    """
    用户登录
    :param request:
    :return:
    """
    try:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        next = request.POST.get('next', '/')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                info = {
                    "is_active": user.is_active,
                    "is_superuser": user.is_staff,
                    "username": user.username,
                }
                result = {"status": 200, "msg": "Login Success", "info": info, "next": next}
                return _response_json(result)
            else:
                result = {"status": 400, "msg": "User is not Active", "info": '', "next": next}
                return _response_json(result)
        else:
            result = {"status": 400, "msg": "User is not exist", "info": '', "next": next}
            return _response_json(result)
    except Exception as e:
        print(e)
        result = {"status": 400, "msg": "Error", "info": '', "next": ''}
        return _response_json(result)


def user_logout(request):
    """
    用户登出
    :param request:
    :return:
    """
    try:
        logout(request)
        result = {"status": 200, "msg": "Logout Success"}
        return _response_json(result)
    except Exception as e:
        print(e)
        result = {"status": 400, "msg": e}
        return _response_json(result)


def signup_user(request):
    """
    注册新用户
    :param request:
    :return:
    """
    email = request.POST.get('email', '')
    username = request.POST.get('username', '')
    password = '123456'
    try:
        # 邮件发送相关
        SMTP_SERVER = 'smtp.qq.com'
        SMTP_SERVER_PORT = 465
        SMTP_USER = '627471266@qq.com'
        SMTP_PSWD = 'azifypvxvurnbecg'
        TO_USERS = email

        title = '新用户注册'
        content = '<html>\
                        <h5>您账号已开通，注册邮箱为' + str(email) + '，登陆信息如下</h5>\
                        <h5>username: ' + str(username) + '</h5>\
                        <h5>password: ' + str(password) + '</h5>\
                        <h5>登陆后请及时更改密码，感谢您的使用！</h5>\
                    </html>'
        try:
            User.objects.create_user(username, email, password)
            if send_mail(SMTP_SERVER, SMTP_SERVER_PORT, SMTP_USER, SMTP_PSWD, TO_USERS, title, content):
                result = {"status": 200, "msg": "SignUp Success"}
                return _response_json(result)
            else:
                result = {"status": 400, "msg": 'SignUp Failed'}
                return _response_json(result)
        except Exception as e:
            print(e)
            result = {"status": 400, "msg": 'Create User Failed：' + e}
            return _response_json(result)
    except Exception as e:
        print(e)
        result = {"status": 400, "msg": e}
        return _response_json(result)


def send_mail(smtp_server, smtp_server_port, smtp_user, smtp_pswd, to_addrs, subject='', text=''):
    """
    发送QQ邮件
    :param smtp_server: SMTP服务器地址
    :param smtp_server_port: SMTP服务器端口
    :param smtp_user: 发送方用户名
    :param smtp_pswd: 发送方客户端密码
    :param to_addrs: 接收方邮箱地址
    :param subject: 邮件标题
    :param text: 邮件内容
    :return:
    """

    msg = MIMEText(text, 'html', 'utf-8')
    msg["Subject"] = subject
    msg["From"] = smtp_user
    msg["To"] = to_addrs
    try:
        s = smtplib.SMTP_SSL(smtp_server, smtp_server_port)
        s.login(smtp_user, smtp_pswd)
        s.sendmail(smtp_user, to_addrs, msg.as_string())
        s.quit()
        return True
    except smtplib.SMTPException as e:
        print(e)
        return False


def change_password(request):
    """
    修改密码
    :param request:
    :return:
    """
    username = request.POST.get('username', '')
    oldpassword = request.POST.get('oldpassword', '')
    newpassword = request.POST.get('newpassword', '')
    try:
        user = authenticate(username=username, password=oldpassword)
        if user is not None:
            if user.is_active:
                user.set_password(newpassword)
                user.save()
                result = {"status": 200, "msg": "Change Password Success"}
                return _response_json(result)
            else:
                result = {'status': 400, 'msg': "The password is valid, but the account has been disabled!"}
                return _response_json(result)
        else:
            result = {'status': 400, 'msg': "The username and password were incorrect"}
            return _response_json(result)
    except Exception as e:
        print(e)
        result = {"status": 400, "msg": e}
        return _response_json(result)


def get_user_list(request):
    """
    获取用户列表
    :return:
    """
    try:
        ret = User.objects.all()
        data = [{"id": i.id, "username": i.username, "last_login": i.last_login, "email": i.email,
                 "is_active": str(i.is_active), "is_superuser": str(i.is_superuser)} for i in ret]
        result = {"status": 200, "data": data, "msg": "Get User List Success"}
        return _response_json(result)
    except Exception as e:
        print(e)
        result = {"status": 400, "msg": e}
        return _response_json(result)


def get_permission_list(request):
    """
    获取权限列表
    :return:
    """
    try:
        ret = Permission.objects.all()
        data = [{"name": i.name, "codename": i.codename, 'id': i.id} for i in ret]
        data.sort(key=lambda x: int(x['id']))
        result = {"status": 200, "data": data, "msg": "Get Permission List Success"}
        return _response_json(result)
    except Exception as e:
        print(e)
        result = {"status": 400, "msg": e}
        return _response_json(result)


def get_group_list(request):
    """
    获取权限组列表
    :return:
    """
    try:
        ret = Group.objects.all()
        data = [{"name": i.name, 'id': i.id} for i in ret]
        data.sort(key=lambda x: int(x['id']))
        result = {"status": 200, "data": data, "msg": "Get Group List Success"}
        return _response_json(result)
    except Exception as e:
        print(e)
        result = {"status": 400, "msg": e}
        return _response_json(result)


def get_group_permission_list(request):
    """
    组权限列表
    :return:
    """
    id = int(request.GET.get('id', ''))
    try:
        data = {}
        query_set = Group.objects.filter(id=id).first()
        own_ret = query_set.permissions.all()
        all_ret = Permission.objects.all()
        data['own_per_list'] = [i.id for index, i in enumerate(own_ret)]
        data['all_per_list'] = [{'label': j.name, 'key': j.id, 'disabled': False} for index, j in enumerate(all_ret)]
        result = {"status": 200, "data": data, "msg": "Get Group List Success"}
        return _response_json(result)
    except Exception as e:
        print(e)
        result = {"status": 400, "msg": e}
        return _response_json(result)


def mod_user_status(request):
    """
    用户激活/冻结
    :return:
    """
    id = request.GET.get('id', '')
    active = request.GET.get('active', 'False')
    is_active = False if active == 'False' else True
    try:
        User.objects.filter(id=id).update(is_active=is_active)
        result = {"status": 200, "data": '', "msg": "Get Group List Success"}
        return _response_json(result)
    except Exception as e:
        print(e)
        result = {"status": 400, "msg": e}
        return _response_json(result)


def change_group_permission_list(request):
    """
    修改组权限列表
    :return:
    """
    group_id = int(request.GET.get('group_id', ''))
    own_per_list = json.loads(request.GET.get('own_per_list', ''))
    try:
        data = {}
        group_obj = Group.objects.get(id=group_id)

        # 旧权限
        old_group = Group.objects.get(id=group_id)
        old_permission = old_group.permissions.all()
        old_per_list = [i.id for i in old_permission]
        old_per_set = set(old_per_list)

        # 新权限
        new_per_set = set(own_per_list)

        # 新旧权限并集
        union_per_set = old_per_set | new_per_set

        # 并集 - 旧权限 = 新增的权限
        add_per_list = list(union_per_set - old_per_set)

        for add_id in add_per_list:
            permission_obj = Permission.objects.get(id=add_id)
            group_obj.permissions.add(permission_obj)

        # 并集 - 新权限 = 删除的权限
        del_per_list = list(union_per_set - new_per_set)

        for del_id in del_per_list:
            permission_obj = Permission.objects.get(id=del_id)
            group_obj.permissions.remove(permission_obj)

        result = {"status": 200, "data": '', "msg": "Change Group List Success"}
        return _response_json(result)
    except Exception as e:
        print(e)
        result = {"status": 400, "msg": e}
        return _response_json(result)


def delete_group_item(request):
    """
    删除权限组
    :return:
    """
    group_id = request.GET.get('group_id', '')
    try:
        Group.objects.get(id=group_id).delete()
        result = {"status": 200, "data": '', "msg": "Get Group List Success"}
        return _response_json(result)
    except Exception as e:
        print(e)
        result = {"status": 400, "msg": e}
        return _response_json(result)


def add_group_item(request):
    """
    添加权限组
    :return:
    """
    group_name = request.GET.get('name', '')
    try:
        Group.objects.create(name=group_name)
        result = {"status": 200, "data": '', "msg": "Add Group Item Success"}
        return _response_json(result)
    except Exception as e:
        print(e)
        result = {"status": 400, "msg": e}
        return _response_json(result)


def get_content_type_list(request):
    """
    获取content type列表
    :return:
    """
    try:
        ret = ContentType.objects.all()
        data = [{'id': i.id, 'label': i.app_label, 'model': i.model} for i in ret]
        data.sort(key=lambda x: int(x['id']))
        result = {"status": 200, "data": data, "msg": "Add Group Item Success"}
        return _response_json(result)
    except Exception as e:
        print(e)
        result = {"status": 400, "msg": e}
        return _response_json(result)


def add_permission_item(request):
    """
    添加权限
    :return:
    """
    name = request.GET.get('name', '')
    codename = request.GET.get('codename', '')
    content_type_id = request.GET.get('app_id', '')
    try:
        Permission.objects.create(name=name, codename=codename, content_type_id=content_type_id)
        result = {"status": 200, "data": '', "msg": "Add Permission Item Success"}
        return _response_json(result)
    except Exception as e:
        print(e)
        result = {"status": 400, "msg": e}
        return _response_json(result)


def del_permission_item(request):
    """
    删除权限
    :return:
    """
    permission_id = request.GET.get('permission_id', '')
    try:
        Permission.objects.get(id=permission_id).delete()
        result = {"status": 200, "data": '', "msg": "Del Permission Item Success"}
        return _response_json(result)
    except Exception as e:
        print(e)
        result = {"status": 400, "msg": e}
        return _response_json(result)


def del_user_item(request):
    """
    删除用户
    :return:
    """
    user_id = request.GET.get('id', '')
    try:
        User.objects.get(id=user_id).delete()
        result = {"status": 200, "data": '', "msg": "Del User Item Success"}
        return _response_json(result)
    except Exception as e:
        print(e)
        result = {"status": 400, "msg": e}
        return _response_json(result)


def get_user_group_list(request):
    """
    获取用户组列表
    :return:
    """
    user_id = int(request.GET.get('user_id', ''))
    try:
        data = {}
        query_set = User.objects.filter(id=user_id).first()
        own_ret = query_set.groups.all()
        all_ret = Group.objects.all()
        data['own_group_list'] = [i.id for index, i in enumerate(own_ret)]
        data['all_group_list'] = [{'label': j.name, 'key': j.id, 'disabled': False} for index, j in enumerate(all_ret)]
        result = {"status": 200, "data": data, "msg": "Get User Group List Success"}
        return _response_json(result)
    except Exception as e:
        print(e)
        result = {"status": 400, "msg": e}
        return _response_json(result)


def mod_user_group_list(request):
    """
    修改用户组列表
    :return:
    """
    user_id = int(request.GET.get('user_id', ''))
    own_group_list = json.loads(request.GET.get('own_group_list', ''))
    try:
        data = {}
        user_obj = User.objects.get(id=user_id)

        # 旧组
        old_user = User.objects.get(id=user_id)
        old_group = old_user.groups.all()
        old_group_list = [i.id for i in old_group]
        old_group_set = set(old_group_list)

        # 新组
        new_group_set = set(own_group_list)

        # 新旧组并集
        union_group_set = old_group_set | new_group_set

        # 并集 - 旧组 = 新增的组
        add_group_list = list(union_group_set - old_group_set)

        for add_id in add_group_list:
            group_obj = Group.objects.get(id=add_id)
            user_obj.groups.add(group_obj)

        # 并集 - 新组 = 删除的组
        del_group_list = list(union_group_set - new_group_set)

        for del_id in del_group_list:
            group_obj = Group.objects.get(id=del_id)
            user_obj.groups.remove(group_obj)

        result = {"status": 200, "data": '', "msg": "Change Group List Success"}
        return _response_json(result)
    except Exception as e:
        print(e)
        result = {"status": 400, "msg": e}
        return _response_json(result)
        return _response_json(result)
