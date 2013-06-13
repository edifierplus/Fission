"""
Fission/urls.py
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Fission.views.home', name='home'),
    # url(r'^Fission/', include('Fission.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^polls/', include('polls.urls', namespace = "polls")),
    url(r'^real/', include('real.urls', namespace = "real")),
    url(r'^admin/', include(admin.site.urls)),
)
