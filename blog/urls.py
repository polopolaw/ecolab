from django.conf.urls import include, url

from . import views
urlpatterns = [
	url(r'<int:slug>/', views.blog_page, name='blog_page')
]