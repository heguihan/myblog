from django.conf.urls import url, include
from django.contrib import admin
from views import *

urlpatterns = [

    # url(r'^$', index),
    # url(r'^article/$', article, name='article'),
    url(r'^$', index, name='index'),
    url(r'^archive/$', archive, name='archive'),
    url(r'^article/$', article, name='article'),
    url(r'^comment_post/$', comment_post, name='comment_post'),
    url(r'^logout$', do_logout, name='logout'),
    # url(r'^reg', do_reg, name='reg'),
    # url(r'^login', do_login, name='login'),
    url(r'^category/$', category, name='category'),
    url(r'^commentgo', commentgo, name='commentgo'),
    url(r'^huifu/$', huifu, name='huifu'),
    url(r'^tag/$', tag, name='tag'),
    url(r'^login/$', login, name='login'),
    url(r'^register/$', register, name='register'),

]
