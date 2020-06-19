from django.conf.urls import include, url

from . import views
urlpatterns = [
	url(r'add_review', views.add_review, name='add_review'),
]