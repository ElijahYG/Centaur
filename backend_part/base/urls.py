"""base URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from backend_part.app.auth.views import auth_views
from backend_part.app import auth_test_views
from backend_part.app.samples.views import sample01_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user_login/', auth_views.user_login),  # check user login
    path('user_logout/', auth_views.user_logout),  # user logout
    path('signup_user/', auth_views.signup_user),  # signup user
    path('change_password/', auth_views.change_password),  # change password
    path('get_user_list/', auth_views.get_user_list),  # get user list
    path('get_permission_list/', auth_views.get_permission_list),  # get permission list
    path('get_group_list/', auth_views.get_group_list),  # get group list
    path('get_group_permission_list/', auth_views.get_group_permission_list),  # get group permission list
    path('mod_user_status/', auth_views.mod_user_status),  # mod user status
    path('change_group_permission_list/', auth_views.change_group_permission_list),  # change group permission list
    path('delete_group_item/', auth_views.delete_group_item),  # delete group item
    path('add_group_item/', auth_views.add_group_item),  # add group item
    path('get_content_type_list/', auth_views.get_content_type_list),  # get content type list
    path('add_permission_item/', auth_views.add_permission_item),  # add permission item
    path('del_permission_item/', auth_views.del_permission_item),  # del permission item
    path('del_user_item/', auth_views.del_user_item),  # del user item
    path('get_user_group_list/', auth_views.get_user_group_list),  # get user group list
    path('mod_user_group_list/', auth_views.mod_user_group_list),  # mod user group list
    # test
    path('test_get_users/', auth_test_views.test_get_users),  # del user item
    # Table Samples
    path('sample01/', sample01_views.sample_table),  # table
]
