from django.conf.urls import include
from django.urls import path
from .feeds import LatestBlogFeed
urlpatterns = [
	path(r'latest/feed/', LatestBlogFeed())
]