"""
real/urls.py
"""
from django.conf.urls import patterns, url
from real import views

urlpatterns = patterns('',
    url(r'^$', views.index, name = 'index'),
    url(r'^build_reactor/$', views.build_reactor, name = 'build_reactor'),
    url(r'^cal_stage/$', views.cal_stage, name = 'cal_stage'),
    url(r'^(?P<reactor_id>\d+)/$', views.show_result, name = 'show_result'),
    url(r'^images/(?P<path>.*)', 'django.views.static.serve',
        {'document_root':'real/images'}),
)
