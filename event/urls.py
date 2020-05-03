from django.conf.urls import include, url

from . import views
urlpatterns = [
	url(r'register', views.register_on_event, name='register_on_event'),
]