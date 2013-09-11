import os
#from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Contacts.views.home', name='home'),
    # url(r'^Contacts/', include('Contacts.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', redirect_to, {'url': '/phonebook/'}),
    url(r'^phonebook/', include('phonebook.urls')),

    (r'^images/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.MEDIA_IMAGES, 'show_indexes': True }),
    (r'^css/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.MEDIA_CSS, 'show_indexes': True }),
    (r'^scripts/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.MEDIA_SCRIPTS, 'show_indexes': True }),
)
