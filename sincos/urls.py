"""
sincos/urls.py
"""
from django.conf.urls import patterns, url
from sincos import views

urlpatterns = patterns('',
    url(r'^$', views.index, name = 'index'),
    url(r'^calculate/$', views.calculate, name = 'calculate'),
    url(r'^(?P<argument_id>\d+)/$', views.result, name = 'result'),
    url(r'^images/(?P<path>.*)', 'django.views.static.serve',
        {'document_root':'sincos/images'}),
)
