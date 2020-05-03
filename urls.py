# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from aldryn_django.utils import i18n_patterns
import aldryn_addons.urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from search import views as search_views



urlpatterns = [
    url(r'^search/$', search_views.search, name='search'),
    url(r'^events/', include('event.urls')),
] + aldryn_addons.urls.patterns() + i18n_patterns(
    # add your own i18n patterns here
    *aldryn_addons.urls.i18n_patterns()  # MUST be the last entry!
)
