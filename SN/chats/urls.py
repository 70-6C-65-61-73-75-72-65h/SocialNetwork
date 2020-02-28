from django.conf.urls import url
from django.urls import re_path
from django.contrib import admin


from .views import (
	chat_list,

    chat_create,

	message_create,
    
	# message_detail,
	# message_update,
	# message_delete,
	# last_10_msgs,
	# message_statistics,
	# answer,
	chat_detail,
	# chat_update,
	chat_delete,
	update_msgs,
	update_chats,
	)
# :chats/create/
# :chats/list/

# :chats/that
# :chats/another

# :chats/msg
urlpatterns = [
    # url(r'^message_create/$', message_create, name='message_create'),
    # ( proflie slugs ) or custom slug based on chat_name created via model form
    url(r'^chat_create/$', chat_create, name='chat_create'), # /(?P<slug>[\w-]+)/(?P<auto>[\d-])

	url(r'^list/$', chat_list, name='chat_list'),

	# url(r'^list/(?P<id>[\w-]+)/forward/$', message_forward, name='message_forward'),

	# should be partly visible ( chat slugs )
	url(r'^chat/(?P<slug>[\w-]+)/$', chat_detail, name='chat_detail'), # enter chat to see msgs and send messagges
    # url(r'^chat/(?P<slug>[\w-]+)/edit/$', chat_update, name='chat_update'), # auto should be
    url(r'^chat/(?P<slug>[\w-]+)/delete/$', chat_delete, name='chat_delete'),

# should be unvisible
    url(r'^chat/(?P<slug>[\w-]+)/message_create/$', message_create, name='message_create'),
    # url(r'^chat/(?P<slug>[\w-]+)/msg/(?P<id>[\w-]+)/$', message_detail, name='message_detail'),
    # url(r'^chat/(?P<slug>[\w-]+)/msg/(?P<id>[\w-]+)/edit/$', message_update, name='message_update'),
    # url(r'^chat/(?P<slug>[\w-]+)/msg/(?P<id>[\w-]+)/delete/$', message_delete, name='message_delete'),

	# url(r'^statictics/', message_statistics, name='message_statistics'),
	# url(r'^thread/(?P<slug>[\w-]+)/answer/$', answer, name='answer'),
	url(r'^chat/(?P<slug>[\w-]+)/update/$', update_msgs, name='update_msgs'), # for 1 chat (like chat detail)

	url(r'^list/update/$', update_chats, name='update_chats'),
]