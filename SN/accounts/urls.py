from django.conf.urls import url, include
from django.urls import re_path
from django.contrib import admin


from .views import (
    login_view, 
    register_view, 
    logout_view,
    profile_view,
    profile_update,
    profile_delete,
    profile_list,
    )

urlpatterns = [
    url(r'^register/', register_view, name='register'),
    url(r'^login/', login_view, name='login'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^profile/(?P<slug>[\w-]+)/$', profile_view, name='profile'),
    url(r'^profile/(?P<slug>[\w-]+)/update/$', profile_update, name='update'),
    url(r'^profile/(?P<slug>[\w-]+)/delete/$', profile_delete, name='delete'),
    url(r'^profile_list/$', profile_list, name='profile_list'),
]