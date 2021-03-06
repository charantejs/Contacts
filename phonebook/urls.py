#from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
import views


urlpatterns = patterns('',
	url(r'^$',views.display_contacts),
	url(r'^search/$',views.search),

	url(r'^add-contact/$',views.add_contact),
	
	url(r'^view-edit-contact/(?P<person_id>\d+)/$',views.view_edit_contact),
	url(r'^delete-contact/(?P<person_id>\d+)/$',views.delete_contact),

	url(r'^add-relationship/$',views.add_relation),

	url('^display-groups/$',views.display_groups),
	url('^add-group/$',views.add_group),
	url('^edit-group/(?P<group_id>\d+)/$',views.edit_group),
	url('^delete-group/(?P<group_id>\d+)/$',views.delete_group),
	url('^view-groupdetails/(?P<group_id>\d+)/$',views.view_groupdetails),
)
