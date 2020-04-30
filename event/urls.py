from django.conf.urls import include, url

from . import views
urlpatterns = [
	url(r'ajax_event_index_page', views.ajax_event_index_page),
]