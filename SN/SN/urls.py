"""SN URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.conf.urls import url, include
# from django.urls import re_path
from django.conf.urls.static import static
from django.conf import settings

from accounts.views import home_view


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),

    url(r'^chats/', include(('chats.urls', 'chats'), namespace='chats')),

    url(r'^posts/', include(('posts.urls', 'posts'), namespace='posts')),
    url(r'^comments/', include(('comments.urls', 'comments'), namespace='comments')),
    url(r'^likes/', include(('likes.urls', 'likes'), namespace='likes')),

    url(r'^password_reset/', include(('password_reset.urls', 'password_reset'), namespace='password_reset')),

    url(r'^$', home_view, name='home'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)